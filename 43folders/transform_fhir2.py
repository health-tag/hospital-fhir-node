import glob
import pandas as pd
import lib.utilitiy as utility
from lib.drug import creatre_allergyIntolerence_resource


# region Dictionary

gender_mapping = {1: "male", 2: "female"}

# endregion

# region Functions

def create_organization_resource(hos_addr, hospcode, hospital_name):
    return {
        "fullUrl": f"urn:uuid:Organization/{hos_addr}",
        "resource": {
            "resourceType": "Organization",
            "identifier": [
                {
                    "system": "https://bps.moph.go.th/hcode/5",
                    "value": f"{hospcode}"
                }
            ],
            "name": f"{hospital_name}"
        },
        "request": {
            "method": "PUT",
            "url": f"Organization/{hos_addr}",
            "ifNoneExist": f"identifier=https://bps.moph.go.th/hcode/5|{hospcode}"
        }
    }

def create_patient_resource(hos_addr, hospcode, person_id, hn, name, surname, folders43_gender):
    patient_identifiers = [
        {
            "system": "https://www.dopa.go.th",
            "value": f"{person_id}"
        },
        {
            "system": "https://sil-th.org/CSOP/hn",
            "value": f"{hn}"
        }
    ]

    gender = gender_mapping[folders43_gender]

    return {
        "fullUrl": f"urn:uuid:Patient/{hospcode}/{hn}",
        "resource": {
            "resourceType": "Patient",
            # "text": {
            #    "status": "extensions",
            #    "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{name} {surname} (HN: {hn})</div>"
            # },
            "identifier": patient_identifiers,
            "name": [
                {
                    "use": "official",
                    # "text": f"{name} {surname}",
                    "family": surname,
                    "given": [
                        name
                    ]
                }
            ],
            "gender": gender,
            "generalPractitioner": [
                {
                    "type": "Organization",
                    "identifier": {
                        "system": "https://bps.moph.go.th/hcode/5",
                        "value": f"{hospcode}"
                    }
                }
            ],
            "managingOrganization": {
                "reference": f"Organization/{hos_addr}"
            }
        },
        "request": {
            "method": "PUT",
            "url": f"Patient?identifier=https://sil-th.org/CSOP/hn|{hn}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/hn|{hn}"
        }
    }
# endregion


# region Configuration
# region Address
hos_addr = '0xC88a594dBB4e9F1ce15d59D0ED129b92E6d89884'
# endregion
#base_fhir_url = 'http://localhost:8000/fhir-api'
base_fhir_url = 'http://localhost:8080/fhir'
headers = {
    'apikey': ''
}
batch_size = 500
# endregion

files = glob.glob("./uploads/*")
person_filename = ''
drugallergy_filename = ''
hospcode = ''
for file in files:
    if 'PERSON' in file:
        person_filename = file

    if 'DRUGALLERGY' in file:
        drugallergy_filename = file
df_person = pd.read_csv(person_filename, encoding="utf8", delimiter="|")
hospcode = df_person["HOSPCODE"][0]
fhir_patient_entries = [create_patient_resource(hos_addr, hospcode=row["HOSPCODE"], person_id=row["CID"], hn=row["HN"],
                                                name=row["NAME"], surname=row["LNAME"], folders43_gender=row["SEX"]) for i, row in df_person.iterrows()]
df_drug_allergy = pd.read_csv(
    drugallergy_filename, encoding="utf8", delimiter="|")
fhir_allergyIntolerance_entries = [y for i, row in df_drug_allergy.iterrows() if (y := creatre_allergyIntolerence_resource(hospcode=hospcode, drug_name=row["DNAME"], drug_dc24=row["DRUGALLERGY"],
                                                                                                                           drug_alevel=row["ALEVEL"], drug_daterecord=row["DATERECORD"], drug_typedx=row["TYPEDX"], drug_symptom=row["SYMPTOM"], patient_cid=row["CID"])) is not None]
print("DRUGALLERGY CSV", len(df_drug_allergy), "items")
print("AllergyIntolerance resource", len(
    fhir_allergyIntolerance_entries), "items")

utility.batch_post_bundule([create_organization_resource(
    hos_addr, hospcode, "TEST Hospital")], base_fhir_url, 1000)
utility.batch_post_bundule(fhir_patient_entries,base_fhir_url,1000)
utility.batch_post_bundule(
    fhir_allergyIntolerance_entries, base_fhir_url, 1000)
