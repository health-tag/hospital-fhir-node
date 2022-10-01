from fhir_transformer.FHIR.Base import FHIRResource
from fhir_transformer.FHIR.Entry import Entry


class Organization(FHIRResource):
    @property
    def name(self) -> str:
        return self._hospital_name

    @property
    def identifier(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "system": "https://bps.moph.go.th/hcode/5",
                "value": f"{self._hospital_code}"
            }
        ]

    def __init__(self, hospital_name: str, hospital_blockchain_address: str, hospital_code: str):
        super(Organization, self).__init__(resource_type="Organization")
        self._hospital_name = hospital_name
        self._hospital_blockchain_address = hospital_blockchain_address
        self._hospital_code = hospital_code

    def create_entry(self) -> Entry:
        entry = Entry(f"Organization/{self._hospital_blockchain_address}", self, {
            "method": "PUT",
            "url": f"Organization/{self._hospital_blockchain_address}",
            "ifNoneExist": f"identifier=https://bps.moph.go.th/hcode/5|{self._hospital_code}"
        })
        return entry

    def __getstate__(self):
        return super().__getstate__()

