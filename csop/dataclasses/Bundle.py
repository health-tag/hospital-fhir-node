from enum import Enum
from Entry import Entry

import jsonpickle


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


oraganizationEntry = Entry.create_organization_entry(hospital_blockchain_address="555", hospital_name="Siriraj",
                                                     hospital_code="X12")
patientEntry = Entry.create_patient_entry("John", "Marstro", "1700", "55", "555", "X12")
patientEntry2 = Entry.create_patient_entry("William", "Runtherford", "1700", "55", "555", "X12")

root_bundle = Bundle(BundleType.Batch, [oraganizationEntry, Bundle(BundleType.Transaction,[patientEntry,patientEntry2])])
print(jsonpickle.encode(root_bundle, unpicklable=False))
