from Base import FHIRResource
from Entry import Entry


class Patient(FHIRResource):
    _name: str
    _surname: str
    _personal_id: str
    _hospital_number: str = None
    _hospital_blockchain_address: str = None
    _hospital_code: str = None
    _member_number: str = None

    @property
    def name(self) -> list[dict[str, str | dict[str, str]]]:
        if (self._combine_name_surname is not None) and (self._combine_name_surname.strip() != ""):
            name_json = [
                {
                    "use": "official",
                    "text": f"{self._combine_name_surname}",
                }
            ]
        else:
            name_json = {
                "use": "official",
                "text": f"{self._name} {self._surname}",
                "family": self._surname,
                "given": [
                    self._name
                ]
            }
        return name_json

    @property
    def identifier(self) -> list[dict[str, str | dict[str, str]]]:
        identity_list = [
            {
                "system": "https://www.dopa.go.th",
                "value": f"{self._personal_id}"
            },
            {
                "system": "https://sil-th.org/CSOP/hn",
                "value": f"{self._hospital_number}"
            }
        ]
        if (self._member_number is not None) and (self._member_number.strip() != ""):
            identity_list.append({
                "system": "https://sil-th.org/CSOP/memberNo",
                "value": f"{self._member_number}"
            })
        return identity_list

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

    def __init__(self, personal_id: str, hospital_number: str,
                 hospital_blockchain_address: str, hospital_code: str, member_number: str = None,
                 combine_name_surname: str = None, name: str = None, surname: str = None):
        super(Patient, self).__init__(resource_type="Patient")
        self._name = name
        self._surname = surname
        self._combine_name_surname = combine_name_surname
        self._personal_id = personal_id
        self._hospital_number = hospital_number
        self._member_number = member_number
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
