from abc import abstractmethod
from enum import Enum
from typing import Any

import jsonpickle

from csop.FHIR.Organization import Organization
from csop.FHIR.Patient import Patient
from csop.FHIR.Entry import Entry


class BundleType(Enum):
    Batch = 1
    Transaction = 2

    def __getstate__(self):
        if self.value == 1:
            return "batch"
        if self.value == 2:
            return "transaction"


class Bundle:
    resourceType = "Bundle"
    type: BundleType
    entry: list[Entry]

    def __init__(self, bundle_type: BundleType, entries: list[Entry]):
        self.type = bundle_type
        self.entry = entries
        self.resourceType = Bundle.resourceType

    def __getstate__(self) -> dict[str, Any]:
        json_dict = self.__dict__.copy()
        return json_dict

# hospital_blockchain_address = "555"
# hospital_name = "Siriraj"
# hospital_code = "X12"
# oraganizationEntry = Organization(hospital_blockchain_address=hospital_blockchain_address, hospital_name=hospital_name,
#                                  hospital_code=hospital_code).create_entry()
# patientEntry = Patient(name="John", surname="Marstro", personal_id="1700", hospital_number="11674",
#                       hospital_blockchain_address=hospital_blockchain_address,
#                       hospital_code=hospital_code).create_entry()
# patientEntry2 = Patient(name="William", surname="Runtherford", personal_id="1700", hospital_number="15546",
#                        hospital_blockchain_address=hospital_blockchain_address,
#                        hospital_code=hospital_code).create_entry()
#
# root_bundle = Bundle(BundleType.Batch,
#                     [oraganizationEntry, Bundle(BundleType.Transaction, [patientEntry, patientEntry2])])
# print(jsonpickle.encode(root_bundle, unpicklable=False))
