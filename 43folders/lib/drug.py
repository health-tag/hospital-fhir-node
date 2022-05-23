import re
import pandas as pd

# region Mapping
dc24totmt_mapping = pd.read_excel("data/rath_drugitems.xlsx")[["name", "did", "sks_drug_code"]].dropna(
    axis="index").set_index("did")["sks_drug_code"].to_dict()
symptom_mapping = pd.read_excel(
    "data/symptom_mapping.xlsx", index_col=0)[["SNOMED CT", "SNOMED NAME"]].to_dict(orient="index")
criticality_mapping = {1: "low", 2: "high", 3: "high",
                       4: "high", 5: "high", 6: "high", 7: "high", 8: "high"}
verificationStatus_mapping = {1: "confirmed", 2: "confirmed",
                              3: "unconfirmed", 4: "unconfirmed", 5: "unconfirmed"}

# endregion

date_regex = re.compile(r"(\d{4})(\d{2})(\d{2})")


def creatre_allergyIntolerence_resource(hospcode, drug_name, drug_dc24, drug_daterecord, drug_alevel, drug_typedx, drug_symptom, patient_cid):
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
    if(drug_dc24 in dc24totmt_mapping):
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
