import re

import xmltodict

from fhir_transformer.csop.holder import BillTransItem, BillTrans, DispensingItemDetail, DispensingItem


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
                # practitioner=license_mapping[item_split[7][0]],
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


