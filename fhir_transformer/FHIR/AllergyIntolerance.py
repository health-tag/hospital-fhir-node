from typing import Dict, List, Any

from fhir_transformer.FHIR.Base import FHIRResource
from fhir_transformer.FHIR.Entry import Entry
from fhir_transformer.mapping_keys.folders43 import verificationStatus_mapping, criticality_mapping, symptom_mapping


class AllergyIntolerance(FHIRResource):
    def __init__(self, patient_cid: str, drug_name: str, drug_id_dc24: str, drug_daterecord: str, drug_alevel: str,
                 drug_typedx: str,
                 drug_symptom: str = None):
        super(AllergyIntolerance, self).__init__(resource_type="AllergyIntolerance")
        self._patient_cid = patient_cid
        self._drug_id_dc24 = drug_id_dc24
        self._drug_typedx = drug_typedx
        self._drug_alevel = drug_alevel
        self.clinicalStatus = AllergyIntolerance.clinicalStatus
        self.category = AllergyIntolerance.category
        if drug_symptom is not None:
            drug_symptom = int(drug_symptom)
            self.reaction = [
                {
                    "manifestation": [
                        {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": symptom_mapping[drug_symptom]["SNOMED CT"],
                                    "display": symptom_mapping[drug_symptom]["SNOMED NAME"]
                                }
                            ]
                        }
                    ]
                }
            ]

    clinicalStatus = {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                "code": "active",
            }
        ]
    }

    @property
    def verificationStatus(self) -> dict[str, list[dict[str, str | Any]]]:
        return {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                    "code": verificationStatus_mapping[self._drug_typedx],
                }
            ]
        }

    category: [
        "medication"
    ]

    @property
    def criticality(self) -> str:
        return criticality_mapping[self._drug_alevel]

    @property
    def code(self) -> None:
        return {
            "coding": [
                {
                    "system": "http://thcc.or.th/homemedicin.php",
                    "code": drug_dc24,
                    "display": drug_name
                }
            ]
        }

    @property
    def patient(self) -> dict[str, str]:
        return {
            "reference": f"Patient?identifier=https://www.dopa.go.th|{patient_cid}"
        }

    @property
    def recordedDate(self) -> str:
        return date_regex.sub(r"\1-\2-\3", str(drug_daterecord))

    def create_entry(self) -> Entry:
        entry = Entry(f"AllergyIntolerance/{self._disp_id}|{self._local_drug_id}", self, {
            "method": "PUT",
            "url": f"AllergyIntolerance?identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}&code=https://sil-th.org/CSOP/localCode|{self._local_drug_id}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/dispenseId|{self._disp_id}&code=https://sil-th.org/CSOP/localCode|{self._local_drug_id}"
        })
        return entry


# region Mapping

# endregion

date_regex = re.compile(r"(\d{4})(\d{2})(\d{2})")


def create_allergyIntolerence_resource(hospcode, drug_name, drug_dc24, drug_daterecord, drug_alevel, drug_typedx,
                                       drug_symptom, patient_cid):
    drug_dc24 = str(drug_dc24)
    allergyIntolerance_resource = {
        "resourceType": "AllergyIntolerance",
        "identifier": [
            {
                "system": "https://www.healthtag.io/coding/allergy-intolerence-dc24",
                "value": f"{patient_cid}-{drug_dc24}"
            }
        ],
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                    "code": "active",
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                    "code": verificationStatus_mapping[drug_typedx],
                }
            ]
        },
        "category": [
            "medication"
        ],
        "criticality": criticality_mapping[drug_alevel],
        "code": {
            "coding": [
                {
                    "system": "http://thcc.or.th/homemedicin.php",
                    "code": drug_dc24,
                    "display": drug_name
                }
            ]
        },
        "patient": {
            "reference": f"Patient?identifier=https://www.dopa.go.th|{patient_cid}"
        },
        "recordedDate": date_regex.sub(r"\1-\2-\3", str(drug_daterecord))
    }
    if (drug_dc24 in dc24totmt_mapping):
        tmt = dc24totmt_mapping[drug_dc24]
        allergyIntolerance_resource["identifier"].append({
            "system": "https://www.healthtag.io/coding/allergy-intolerence-tmt",
            "value": f"{patient_cid}-{tmt}"
        })
        allergyIntolerance_resource["code"]["coding"].append({
            "system": "https://www.this.or.th/tmt_about.php",
            "code": tmt,
            "display": drug_name
        })
    if not pd.isna(drug_symptom):
        drug_symptom = int(drug_symptom)
        allergyIntolerance_resource["reaction"] = [
            {
                "manifestation": [
                    {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": symptom_mapping[drug_symptom]["SNOMED CT"],
                                "display": symptom_mapping[drug_symptom]["SNOMED NAME"]
                            }
                        ]
                    }
                ]
            }
        ]
    a = {
        "fullUrl": f"urn:uuid:AllergyIntolerance/{patient_cid}-{drug_dc24}",
        "resource": allergyIntolerance_resource,
        "request": {
            "method": "PUT",
            "url": f"AllergyIntolerance?identifier=https://www.healthtag.io/coding/allergy-intolerence-dc24|{patient_cid}-{drug_dc24}",
            "ifNoneExist": f"identifier=https://www.healthtag.io/coding/allergy-intolerence-dc24|{patient_cid}-{drug_dc24}"
        }
    }
    return a
