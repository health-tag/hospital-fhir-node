import re
import xmltodict


class BillTrans:
    hospital_code:str
    hospital_name:str

    def __init__(self, hospital_code:str, hospital_name:str):
        self.hospital_code = hospital_code
        self.hospital_name = hospital_name


def get_file_encoding(file_path):
    with open(file_path) as xml_file_for_encoding_check:
        first_line = xml_file_for_encoding_check.readline()
        encoding = re.search('encoding="(.*)"', first_line).group(1)
        if encoding == "windows-874":
            encoding = "cp874"
        return encoding


def open_bill_trans_xml(file_path: str):
    with open(file_path, get_file_encoding(file_path)) as xml_file:
        dict = xmltodict.parse(xml_file.read())
        hospital_code = dict['ClaimRec']['Header']['HCODE']
        hospital_name = dict['ClaimRec']['Header']['HNAME']
        bill_trans = BillTrans(hospital_code, hospital_name)


with open(bill_trans, encoding=bill_trans_encoding) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    h_code = data_dict['ClaimRec']['Header']['HCODE']
    h_name = data_dict['ClaimRec']['Header']['HNAME']
    bill_trans = data_dict['ClaimRec']['BILLTRAN'].split('\n')
    bill_trans_items = data_dict['ClaimRec']['BillItems'].split('\n')
    for item in bill_trans:
        item_split = item.split('|')
        item_data = {
            'station': item_split[0],
            'inv_no': item_split[4],
            'hn': item_split[6],
            'member_no': item_split[7],
            'pid': item_split[12],
            'name': item_split[13],
            'pay_plan': item_split[15],
        }
        tran_items[item_data['inv_no']] = item_data
