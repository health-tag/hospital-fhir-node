from fhir_transformer.FHIR.Base import FHIRResource
from fhir_transformer.FHIR.Entry import Entry
from fhir_transformer.mapping_keys.csop import disp_status_mapping


class EncounterDispensing(FHIRResource):
    def __init__(self, disp_id: str, presc_date: str, disp_date: str, disp_status: str,
                 belonged_to_hospital_number: str, practitioner_system: str, practitioner_license_number_part: str,
                 hospital_code: str, hospital_blockchain_address: str):
        super(EncounterDispensing, self).__init__(resource_type="Encounter")
        self._disp_id = disp_id
        self._presc_date = presc_date
        self._disp_date = disp_date
        self._disp_status = disp_status
        self._belonged_to_hospital_number = belonged_to_hospital_number
        self._practitioner_system = practitioner_system
        self._practitioner_license_number_part = practitioner_license_number_part
        self._hospital_code = hospital_code
        self._hospital_blockchain_address = hospital_blockchain_address

        self.status = EncounterDispensing.status
        self._reserved_class = EncounterDispensing._reserved_class
        self.serviceType = EncounterDispensing.serviceType

    def create_entry(self) -> Entry:
        entry = Entry(f"Encounter/{self._disp_id}", self, {
            "method": "PUT",
            "url": f"Encounter?identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}"
        })
        return entry

    def __getstate__(self):
        return super().__getstate__()

    @property
    def text(self) -> dict[str, str]:
        return {
            "status": "extensions",
            "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Dispense ID: {self._disp_id} (HN: {self._belonged_to_hospital_number})<p>service: Pharmacy | status: {disp_status_mapping[self._disp_status]}</p></div>"
        }

    @property
    def identifier(self) -> list[dict[str, str]]:
        return [
            {
                "system": "https://sil-th.org/CSOP/dispenseId",
                "value": f"{self._disp_id}"
            }
        ]

    status = "finished",
    _reserved_class = {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": "AMB"
    }
    serviceType = {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/service-type",
                "code": "64",
                "display": "Pharmacy"
            }
        ]
    }

    @property
    def subject(self) -> dict[str, str]:
        return {
            "reference": f"Patient?identifier=https://sil-th.org/CSOP/hn|{self._belonged_to_hospital_number}"
        }

    @property
    def participant(self) -> list[dict[str, dict[str, str]]]:
        return [
            {
                "individual": {
                    "reference": f"Practitioner?identifier={self._practitioner_system}|{self._practitioner_license_number_part}"
                }
            }
        ]

    @property
    def period(self) -> dict[str, str]:
        return {
            "start": f"{self._presc_date}",
            "end": f"{self._disp_date}"
        }

    @property
    def serviceProvider(self) -> dict[str, str]:
        return {
            "reference": f"Organization/{self._hospital_blockchain_address}"
        }
