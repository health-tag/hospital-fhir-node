from enum import Enum
from Entry import Entry

import jsonpickle

from Organization import Organization
from Patient import Patient


class BundleType(Enum):
    Batch = 1
    Transaction = 2

    def __getstate__(self):
        if self.value == 1:
            return "batch"
        if self.value == 2:
            return "Transaction"


class Bundle:
    bundleType: BundleType
    entry: list[Entry]

    def __init__(self, bundle_type: BundleType, entries: list[Entry]):
        self.bundleType = bundle_type
        self.entry = entries


hospital_blockchain_address = "555"
hospital_name = "Siriraj"
hospital_code = "X12"
oraganizationEntry = Organization(hospital_blockchain_address=hospital_blockchain_address, hospital_name=hospital_name,
                                  hospital_code=hospital_code).create_entry()
patientEntry = Patient(name="John", surname="Marstro", personal_id="1700", hospital_number="11674",
                       hospital_blockchain_address=hospital_blockchain_address, hospital_code=hospital_code).create_entry()
patientEntry2 = Patient(name="William", surname="Runtherford", personal_id="1700", hospital_number="15546",
                        hospital_blockchain_address=hospital_blockchain_address, hospital_code=hospital_code).create_entry()

root_bundle = Bundle(BundleType.Batch,
                     [oraganizationEntry, Bundle(BundleType.Transaction, [patientEntry, patientEntry2])])
print(jsonpickle.encode(root_bundle, unpicklable=False))
