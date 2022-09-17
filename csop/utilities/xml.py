import re
from dataclasses import dataclass

import jsonpickle
import requests
import xmltodict

from csop.FHIR.Bundle import Bundle, BundleType
from csop.FHIR.Encounter import EncounterDispensing
from csop.FHIR.Location import Location
from csop.FHIR.MedicationDispense import MedicationDispense
from csop.FHIR.Organization import Organization
from csop.FHIR.Patient import Patient
from csop.FHIR.Practitioner import Practitioner
from csop.utilities.mapping_key import license_mapping
from csop.utilities.networking import send_bundle

# CONFIG SHOULD MOVE OUT OF THIS FILE
hospital_blockchain_address = '0xC88a594dBB4e9F1ce15d59D0ED129b92E6d89884'


@dataclass
class BillTransItem:
    station: str
    inv_no: str
    hn: str
    member_no: str
    pid: str
    name: str
    pay_plan: str


@dataclass
class BillTrans:
    hospital_code: str
    hospital_name: str
    items_dict: dict[str, BillTransItem]


@dataclass
class DispensingItemDetail:
    disp_id: str
    product_cat: str
    local_drug_id: str
    standard_drug_id: str
    dfs: str
    package_size: str
    instruction_code: str
    instruction_text: str
    quantity: str
    # 'prd_code': item_split[14],
    # 'multiple_disp': item_split[17],
    # 'supply_for': item_split[18],


class DispensingItem:
    _practitioner: str

    @property
    def practitioner(self):
        return license_mapping[self._practitioner]

    def __init__(self, provider_id: str, disp_id: str, inv_no: str, presc_date: str, disp_date: str, license_id: str,
                 disp_status: str, practitioner: str, items: list[DispensingItemDetail]):
        self.items = items
        self._practitioner = practitioner
        self.disp_status = disp_status
        self.license_id = license_id
        self.disp_date = disp_date
        self.presc_date = presc_date
        self.inv_no = inv_no
        self.disp_id = disp_id
        self.provider_id = provider_id


def _get_file_encoding(file_path):
    with open(file_path) as xml_file_for_encoding_check:
        first_line = xml_file_for_encoding_check.readline()
        encoding = re.search('encoding="(.*)"', first_line).group(1)
        if encoding == "windows-874":
            encoding = "cp874"
        return encoding


def _open_bill_trans_xml(file_path: str):
    with open(file_path, encoding=_get_file_encoding(file_path)) as xml_file:
        xml_dict = xmltodict.parse(xml_file.read())
        tran_items = dict()
        hospital_code = xml_dict['ClaimRec']['Header']['HCODE']
        hospital_name = xml_dict['ClaimRec']['Header']['HNAME']
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
            tran_items[item_data.inv_no] = item_data
        return BillTrans(hospital_code, hospital_name, tran_items)


def _open_bill_disp_xml(file_path: str):
    with open(file_path, encoding=_get_file_encoding(file_path)) as xml_file:
        xml_dict = xmltodict.parse(xml_file.read())
        disp_items = dict()
        main_disps = xml_dict['ClaimRec']['Dispensing'].split('\n')
        detail_disps = xml_dict['ClaimRec']['DispensedItems'].split('\n')
        for item in main_disps:
            item_split = item.split('|')
            item_data = DispensingItem(
                provider_id=item_split[0],
                disp_id=item_split[1],
                inv_no=item_split[2],
                presc_date=item_split[5],
                disp_date=item_split[6],
                license_id=item_split[7],
                disp_status=item_split[15],
                practitioner=license_mapping[item_split[7][0]],
                items=list()
            )
            disp_items[item_data.disp_id] = item_data
        for item in detail_disps:
            item_split = item.split('|')
            item_details_data = DispensingItemDetail(
                disp_id=item_split[0],
                product_cat=item_split[1],
                local_drug_id=item_split[2],
                standard_drug_id=item_split[3],
                dfs=item_split[5],
                package_size=item_split[6],
                instruction_code=item_split[7],
                instruction_text=item_split[8],
                quantity=item_split[9],
                # 'prd_code': item_split[14],
                # 'multiple_disp': item_split[17],
                # 'supply_for': item_split[18],
            )
            current_items = disp_items[item_details_data.disp_id].items
            current_items.append(item_details_data)
        return disp_items


def process(bill_trans_xml_path: str, bill_disp_xml_path: str):
    bill_trans_xml_data = _open_bill_trans_xml(bill_trans_xml_path)
    bill_disp_xml_data = _open_bill_disp_xml(bill_disp_xml_path)

    # region GENERATE + SEND ONE ORGANIZATION DATA
    organization_bundle = Bundle(BundleType.Batch,
                                 [Organization(bill_trans_xml_data.hospital_name, hospital_blockchain_address,
                                               bill_trans_xml_data.hospital_code).create_entry()])

    send_bundle(organization_bundle)
    # endregion GENERATE + SEND ONE ORGANIZATION DATA

    # region GENERATE + SEND UNIQUE LOCATION DATA
    locations = dict()
    for inv_no, bill_trans_item in bill_trans_xml_data.items_dict.items():
        locations[bill_trans_item.station] = Location(station=bill_trans_item.station,
                                                      hospital_blockchain_address=hospital_blockchain_address)
    locations_bundle = Bundle(BundleType.Batch, [entry.create_entry() for entry in list(locations.values())])
    send_bundle(locations_bundle)
    # endregion GENERATE + SEND UNIQUE LOCATION DATA

    # region Generate FHIR Resource for each person
    practitioners = dict()
    patients: dict[str, Patient] = dict()
    encounters: dict[str, list[EncounterDispensing]] = dict()
    medicationDispenses: dict[str, list[MedicationDispense]] = dict()
    for disp_id, bill_disp_item in bill_disp_xml_data.items():
        corresponding_bill_trans_item = bill_trans_xml_data.items_dict[bill_disp_item.inv_no]
        # GENERATE UNIQUE PRACTITIONER
        practitioners[bill_disp_item.license_id] = Practitioner(license_id=bill_disp_item.license_id)
        # GENERATE PATIENT
        patient = Patient(combine_name_surname=corresponding_bill_trans_item.name,
                          personal_id=corresponding_bill_trans_item.pid,
                          hospital_number=corresponding_bill_trans_item.hn,
                          hospital_blockchain_address=hospital_blockchain_address,
                          hospital_code=bill_trans_xml_data.hospital_code,
                          member_number=corresponding_bill_trans_item.member_no)
        patients[corresponding_bill_trans_item.pid] = patient
        encounters[corresponding_bill_trans_item.pid] = list()
        medicationDispenses[corresponding_bill_trans_item.pid] = list()
        for bill_disp_item_detail in bill_disp_item.items:
            encounter = EncounterDispensing(disp_id=bill_disp_item_detail.disp_id,
                                            presc_date=bill_disp_item.presc_date, disp_date=bill_disp_item.disp_date,
                                            disp_status=bill_disp_item.disp_status,
                                            belonged_to_hospital_number=corresponding_bill_trans_item.hn,
                                            practitioner_system=practitioners[
                                                bill_disp_item.license_id].license_system.system,
                                            practitioner_license_number_part=practitioners[
                                                bill_disp_item.license_id].license_number_part,
                                            hospital_code=bill_trans_xml_data.hospital_code,
                                            hospital_blockchain_address=hospital_blockchain_address)
            encounters[corresponding_bill_trans_item.pid].append(encounter)
            medicationDispense = MedicationDispense(disp_id=bill_disp_item_detail.disp_id,
                                                    disp_status=bill_disp_item.disp_status,
                                                    local_drug_id=bill_disp_item_detail.local_drug_id,
                                                    standard_drug_id=bill_disp_item_detail.standard_drug_id,
                                                    product_cat=bill_disp_item_detail.product_cat,
                                                    disp_date=bill_disp_item.disp_date,
                                                    dfs=bill_disp_item_detail.dfs,
                                                    quantity=bill_disp_item_detail.quantity,
                                                    package_size=bill_disp_item_detail.package_size,
                                                    instruction_text=bill_disp_item_detail.instruction_text,
                                                    instruction_code=bill_disp_item_detail.instruction_code,
                                                    belonged_to_hospital_number=corresponding_bill_trans_item.hn,
                                                    hospital_code=bill_trans_xml_data.hospital_code,
                                                    hospital_blockchain_address=hospital_blockchain_address)
            medicationDispenses[corresponding_bill_trans_item.pid].append(medicationDispense)
    # SEND PRACTITIONERS
    practitioners_bundle = Bundle(BundleType.Batch, [entry.create_entry() for entry in list(practitioners.values())])
    send_bundle(practitioners_bundle)
    # PREPARE PATIENT + ENCOUNTER + MEDICAL DISPENSING
    patient_transaction_bundle = list()
    for key in patients.keys():
        entry = list()
        entry = entry + [patients[key].create_entry()]
        if key in encounters:
            entry = entry + [encounter.create_entry() for encounter in encounters[key]]
        if key in medicationDispenses:
            entry = entry + [medication_dispense.create_entry() for medication_dispense in medicationDispenses[key]]
        patient_transaction_bundle.append(Bundle(BundleType.Transaction, entry))
    # SEND PATIENT + ENCOUNTER + MEDICAL DISPENSING
    send_bundle(Bundle(BundleType.Batch,patient_transaction_bundle))
    # endregion
