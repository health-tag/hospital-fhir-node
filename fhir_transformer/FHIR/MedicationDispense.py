from fhir_transformer.FHIR.Base import FHIRResource
from fhir_transformer.FHIR.Entry import Entry
from fhir_transformer.mapping_keys.csop import disp_status_mapping


class MedicationDispense(FHIRResource):
    def __init__(self, disp_id: str, disp_status: str, local_drug_id: str, standard_drug_id: str, product_cat: str,
                 dfs: str,
                 quantity: str, package_size: str, disp_date: str,
                 instruction_text: str, instruction_code: str,
                 belonged_to_hospital_number: str, hospital_code: str, hospital_blockchain_address: str):
        super(MedicationDispense, self).__init__(resource_type="MedicationDispense")

        self._disp_id = disp_id
        self._disp_status = disp_status
        self._local_drug_id = local_drug_id
        self._standard_drug_id = standard_drug_id
        self._product_cat = product_cat
        self._dfs = dfs
        self._quantity = quantity
        self._package_size = package_size
        self._instruction_text = instruction_text
        self._instruction_code = instruction_code
        self.category = MedicationDispense.category
        self.whenHandedOver = disp_date

        self._belonged_to_hospital_number = belonged_to_hospital_number
        self._hospital_code = hospital_code
        self._hospital_blockchain_address = hospital_blockchain_address

    def create_entry(self) -> Entry:
        entry = Entry(f"MedicationDispense/{self._disp_id}|{self._local_drug_id}", self, {
            "method": "PUT",
            "url": f"MedicationDispense?identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}&code=https://sil-th.org/CSOP/localCode|{self._local_drug_id}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}&code=https://sil-th.org/CSOP/localCode|{self._local_drug_id}"
        })
        return entry

    def __getstate__(self):
        return super().__getstate__()

    @property
    def text(self) -> dict[str, str]:
        return {
            "status": "extensions",
            "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">Dispense ID: {self._disp_id} (HN: {self._belonged_to_hospital_number})<p>{self._dfs} - {self._instruction_text}</p><p>QTY: {self._quantity} {self._package_size}</p></div>"
        }

    @property
    def extension(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "url": "https://sil-th.org/fhir/StructureDefinition/product-category",
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "https://sil-th.org/fhir/CodeSystem/csop-productCategory",
                            "code": f"{self._product_cat}"
                        }
                    ]
                }
            },
        ]

    @property
    def identifier(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "system": "https://sil-th.org/CSOP/dispenseId",
                "value": f"{self._disp_id}"
            }
        ]

    @property
    def status(self) -> str:
        return f"{disp_status_mapping[self._disp_status]}"

    category = {
        "coding": [
            {
                "system": "http://terminology.hl7.org/fhir/CodeSystem/medicationdispense-category",
                "code": "outpatient"
            }
        ]
    }

    @property
    def medicationCodeableConcept(self) -> dict[str, str]:
        return {
            "coding": [
                {
                    "system": "https://sil-th.org/CSOP/localCode",
                    "code": f"{self._local_drug_id}"
                },
                {
                    "system": "https://tmt.this.or.th",
                    "code": f"{self._standard_drug_id}"
                }
            ],
            "text": f"{self._dfs}"
        }

    @property
    def subject(self) -> dict[str, str]:
        return {
            "reference": f"Patient?identifier=https://sil-th.org/CSOP/hn|{self._belonged_to_hospital_number}",
        }

    @property
    def context(self) -> dict[str, str]:
        return {
            "reference": f"Encounter?identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}"
        }

    @property
    def performer(self) -> list[dict[str, dict[str, str]]]:
        return [
            {
                "actor": {
                    "reference": f"Organization/{self._hospital_blockchain_address}"
                }
            }
        ]

    @property
    def quantity(self) -> dict[str, set[str]]:
        return {
            "value": {self._quantity},
            "unit": {self._package_size}
        }

    @property
    def dosageInstruction(self) -> list[dict[str, str]]:
        return [
            {
                "text": f"{self._instruction_text}",
                "timing": {
                    "code": {
                        "text": f"{self._instruction_code}"
                    }
                }
            }
        ]
