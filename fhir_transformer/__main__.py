import glob
import json
import platform
import sys
import pathlib

from dataclasses import dataclass

import jsonpickle

from fhir_transformer.csop.processor import process


@dataclass
class FilePair:
    bill_trans_path: str
    bill_disp_path: str


def banner():
    print("**********************************")
    print("* HealthTAG FHIR Transformer v.2 *")
    print("*      18 September 2022         *")
    print("*         healthtag.io           *")
    print("*      support@healthtag.io      *")
    print("**********************************")


def run():
    banner()
    slash = "\\" if platform.system() == "Windows" else "/"
    print(f"Converting CSOP Files in {slash}uploads{slash}csop{slash}")
    files = glob.glob(f".{slash}uploads{slash}csop{slash}**{slash}**")
    if len(files) == 0:
        print(f"No file found in .{slash}uploads{slash}csop{slash}")
    else:
        print(f"{len(files)} file found in .{slash}uploads{slash}csop{slash}")
        for file in files:
            print(file)
        print(f"Try matching the files")
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
        date = uppercase_file[uppercase_file.index("BILLTRAN") + len("BILLTRAN"): uppercase_file.rindex(".")]
        for bill_disp_file in bill_disp_files:
            if date in bill_disp_file:
                files_pair[date] = FilePair(bill_trans_path=bill_trans_file, bill_disp_path=bill_disp_file)

    for key, file_pair in files_pair.items():
        print(f"PROCESSING {key} => {file_pair.bill_trans_path} AND {file_pair.bill_disp_path}")
        result = process(bill_trans_xml_path=file_pair.bill_trans_path,
                         bill_disp_xml_path=file_pair.bill_disp_path)
        directory = pathlib.Path(file_pair.bill_trans_path).parent.resolve()
        with open(f"{directory}{slash}result.json", "w") as out_file:
            out_file.write(jsonpickle.encode(result, unpicklable=False, indent=True))


if __name__ == '__main__':
    sys.exit(run())
