from typing import List, Dict

from Base import FHIRResource
from Entry import Entry


class Patient(FHIRResource):
    name = None
    identifier = None
    generalPractitioner = None
    managingOrganization = None

    _name: str
    _surname: str
    _thai_citizen_id: str
    _hospital_number: str = None
    _hospital_blockchain_address: str = None
    _hospital_code: str = None

    @property
    def name(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "use": "official",
                # "text": f"{name} {surname}",
                "family": self._surname,
                "given": [
                    self._name
                ]
            }
        ]

    @property
    def identifier(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "system": "https://www.dopa.go.th",
                "value": f"{self._thai_citizen_id}"
            },
            {
                "system": "https://sil-th.org/CSOP/hn",
                "value": f"{self._hospital_number}"
            }
        ]

    @property
    def generalPractitioner(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "type": "Organization",
                "identifier": {
                    "system": "https://bps.moph.go.th/hcode/5",
                    "value": f"{self._hospital_code}"
                }
            }
        ]

    @property
    def managingOrganization(self) -> dict[str, str]:
        return {
            "reference": f"Organization/{self._hospital_blockchain_address}"
        }

    def __init__(self, name: str, surname: str, thai_citizen_id: str, hospital_number: str,
                 hospital_blockchain_address: str, hospital_code: str):
        super(Patient, self).__init__(resource_type="Patient")
        self._name = name
        self._surname = surname
        self._thai_citizen_id = thai_citizen_id
        self._hospital_number = hospital_number
        self._hospital_blockchain_address = hospital_blockchain_address
        self._hospital_code = hospital_code

    def create_entry(self) -> Entry:
        entry = Entry(f"urn:uuid:Patient/{self._hospital_code}/{self._hospital_number}", self, {
            "method": "PUT",
            "url": f"Patient?identifier=https://sil-th.org/CSOP/hn|{self._hospital_number}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/hn|{self._hospital_number}"
        })
        return entry

    def __getstate__(self):
        return super.__getstate__(self)
