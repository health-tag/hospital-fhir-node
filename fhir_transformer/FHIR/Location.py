from typing import Dict, List

from fhir_transformer.FHIR.Base import FHIRResource
from fhir_transformer.FHIR.Entry import Entry


class Location(FHIRResource):
    def __init__(self, station: str, hospital_blockchain_address: str):
        super(Location, self).__init__(resource_type="Location")
        self._station = station
        self._hospital_blockchain_address = hospital_blockchain_address

    def create_entry(self) -> Entry:
        entry = Entry(f"Location?identifier=https://sil-th.org/CSOP/station|{self._station}", self, {
            "method": "PUT",
            "url": f"Location?identifier=https://sil-th.org/CSOP/station|{self._station}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/station|{self._station}"
        })
        return entry

    def __getstate__(self):
        return super().__getstate__()

    @property
    def text(self) -> dict[str, str]:
        return {
            "status": "generated",
            "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Station ID: {self._station}</div>"
        }

    @property
    def identifier(self) -> list[dict[str, str]]:
        return [
            {
                "system": "https://sil-th.org/CSOP/station",
                "value": f"{self._station}"
            }
        ]

    @property
    def type(self) -> list[dict[str, list[dict[str, str]]]]:
        return [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                        "code": "BILL",
                        "display": "Billing Contact"
                    }
                ]
            }
        ]

    @property
    def managingOrganization(self) -> dict[str, str]:
        return {
            "reference": f"Organization/{self._hospital_blockchain_address}"
        }
