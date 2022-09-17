import glob
from dataclasses import dataclass

from fhir_transformer.utilities.xml import process


@dataclass
class FilePair:
    bill_trans_path: str
    bill_disp_path: str


files = glob.glob("./uploads/*")

files_pair: dict[str, FilePair] = dict()
bill_trans_files = list()
bill_disp_files = list()
for file in files:
    if "BILLTRAN" in file.upper():
        bill_trans_files.append(file)
    if "BILLDISP" in file.upper():
        bill_disp_files.append(file)
for bill_trans_file in bill_trans_files:
    uppercase_file = bill_trans_file.upper()
    date = uppercase_file[uppercase_file.index("BILLTRAN")+len("BILLTRAN"): uppercase_file.rindex(".")]
    for bill_disp_file in bill_disp_files:
        if date in bill_disp_file:
            files_pair[date] = FilePair(bill_trans_path=bill_trans_file, bill_disp_path=bill_disp_file)

for key, file_pair in files_pair.items():
    print(f"PROCESSING {key}")
    process(bill_trans_xml_path=file_pair.bill_trans_path,
            bill_disp_xml_path=file_pair.bill_disp_path)
