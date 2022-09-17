import re

import jsonpickle
import requests
import xmltodict

from csop.dataclasses.Bundle import Bundle, BundleType
from csop.dataclasses.MedicationDispense import MedicationDispense
from csop.dataclasses.Organization import Organization
from csop.dataclasses.Patient import Patient
from csop.utilities.mapping_key import license_mapping
from csop.utilities.networking import send_bundle

# CONFIG SHOULD MOVE OUT OF THIS FILE
hospital_blockchain_address = '0xC88a594dBB4e9F1ce15d59D0ED129b92E6d89884'
base_fhir_url = 'http://localhost:8080/fhir'
headers = {
    'apikey': ''
}


class BillTransItem:
    def __init__(self, station: str, inv_no: str, hn: str, member_no: str, pid: str, name: str, pay_plan: str):
        self.pay_plan = pay_plan
        self.name = name
        self.pid = pid
        self.member_no = member_no
        self.hn = hn
        self.inv_no = inv_no
        self.station = station


class BillTrans:
    hospital_code: str
    hospital_name: str
    items: dict[str, BillTransItem] = None

    def __init__(self, hospital_code: str, hospital_name: str):
        self.hospital_code = hospital_code
        self.hospital_name = hospital_name


class DispensingItemDetail:

    def __init__(self,disp_id:str,product_cat:str,local_drug_id:str,standard_drug_id:str,dfs:str,package_size:str,instruction_code:str,instruction_text:str,quantity:str):

    'disp_id': item_split[0],
    'product_cat': item_split[1],
    'local_drug_id': item_split[2],
    'standard_drug_id': item_split[3],
    'dfs': item_split[5],
    'package_size': item_split[6],
    'instruction_code': item_split[7],
    'instruction_text': item_split[8],
    'quantity': item_split[9],
    # 'prd_code': item_split[14],
    # 'multiple_disp': item_split[17],
    # 'supply_for': item_split[18],

class DispensingItem:
    _practitioner:str
    @property
    def practitioner(self):
        return license_mapping[self._practitioner]

    def __init__(self, provider_id: str, disp_id: str, inv_no: str, presc_date: str, disp_date: str, license_id: str, disp_status: str, practitioner:str, items: DispensingItemDetail[]):
        self.items = items
        self._practitioner = practitioner
        self.disp_status = disp_status
        self.license_id = license_id
        self.disp_date = disp_date
        self.presc_date = presc_date
        self.inv_no = inv_no
        self.disp_id = disp_id
        self.provider_id = provider_id

def get_file_encoding(file_path):
    with open(file_path) as xml_file_for_encoding_check:
        first_line = xml_file_for_encoding_check.readline()
        encoding = re.search('encoding="(.*)"', first_line).group(1)
        if encoding == "windows-874":
            encoding = "cp874"
        return encoding


def open_bill_trans_xml(file_path: str):
    with open(file_path, get_file_encoding(file_path)) as xml_file:
        xml_dict = xmltodict.parse(xml_file.read())
        tran_items = dict()
        hospital_code = xml_dict['ClaimRec']['Header']['HCODE']
        hospital_name = xml_dict['ClaimRec']['Header']['HNAME']
        obj = BillTrans(hospital_code, hospital_name)
        bill_trans = xml_dict['ClaimRec']['BILLTRAN'].split('\n')
        bill_trans_items = xml_dict['ClaimRec']['BillItems'].split('\n')
        for item in bill_trans:
            item_split = item.split('|')
            item_data = BillTransItem(
                station=item_split[0],
                inv_no=item_split[4],
                hn=item_split[6],
                member_no=item_split[7],
                pid=item_split[12],
                name=item_split[13],
                pay_plan=item_split[15],
            )
            tran_items[item_data['inv_no']] = item_data
        obj.items = tran_items
        return obj


def open_bill_disp_xml(file_path: str):
    with open(file_path, get_file_encoding(file_path)) as xml_file:
        xml_dict = xmltodict.parse(xml_file.read())
        disp_items = dict()
        main_disps = xml_dict['ClaimRec']['Dispensing'].split('\n')
        detail_disps = xml_dict['ClaimRec']['DispensedItems'].split('\n')
        for item in main_disps:
            item_split = item.split('|')
            item_data = {
                'provider_id': item_split[0],
                'disp_id': item_split[1],
                'inv_no': item_split[2],
                'presc_date': item_split[5],
                'disp_date': item_split[6],
                'license_id': item_split[7],
                'disp_status': item_split[15],
                'practitioner': license_mapping[item_split[7][0]],
                'items': []
            }
            disp_items[item_data['disp_id']] = item_data
        for item in detail_disps:
            item_split = item.split('|')
            item_details_data = {
                'disp_id': item_split[0],
                'product_cat': item_split[1],
                'local_drug_id': item_split[2],
                'standard_drug_id': item_split[3],
                'dfs': item_split[5],
                'package_size': item_split[6],
                'instruction_code': item_split[7],
                'instruction_text': item_split[8],
                'quantity': item_split[9],
                # 'prd_code': item_split[14],
                # 'multiple_disp': item_split[17],
                # 'supply_for': item_split[18],
            }
            current_items = disp_items[item_details_data['disp_id']]['items']
            current_items.append(item_details_data)
            disp_items[item_details_data['disp_id']]['items'] = current_items
        return disp_items


def execute(bill_trans_xml_path: str, bill_disp_xml_path: str):
    bill_trans_data = open_bill_trans_xml(bill_trans_xml_path)
    bill_disp_xml_data = open_bill_disp_xml(bill_disp_xml_path)

    # SEND ORGANIZATION DATA
    oraganization_bundle = Bundle(BundleType.Batch,
                                  [Organization(bill_trans_data.hospital_name, hospital_blockchain_address,
                                                bill_trans_data.hospital_code).create_entry()])
    send_bundle(oraganization_bundle)

    # Generate FHIR Resource for each person
    for disp_id, info in bill_disp_xml_data.items():
        bill_trans_item = bill_trans_data.items[info['inv_no']]
        combined_data = {**info}
        Patient(combine_name_surname=bill_trans_item.name, personal_id=bill_trans_item.pid,
                hospital_number=bill_trans_item.hn, hospital_blockchain_address=hospital_blockchain_address,
                hospital_code=bill_trans_data.hospital_code, member_number=bill_trans_item.member_no)
        MedicationDispense()
