import math
from datetime import datetime

from fhir_transformer.FHIR.Bundle import BundleType, Bundle
from fhir_transformer.FHIR.Encounter import EncounterDispensing
from fhir_transformer.FHIR.Location import Location
from fhir_transformer.FHIR.MedicationDispense import MedicationDispense
from fhir_transformer.FHIR.Organization import Organization
from fhir_transformer.FHIR.Patient import Patient
from fhir_transformer.FHIR.Practitioner import Practitioner
from fhir_transformer.utilities.networking import send_bundle

hospital_blockchain_address = "bx123456789"
hospital_name = "Test"
hospital_code = "5786"
license_id = "ว54321"
doctor = Practitioner(license_id=license_id)
station = "12"
print(f"PREPARE AND SENDING ORGANIZATION {datetime.now()}")
organization_bundle = Bundle(BundleType.Batch,
                             [Organization(hospital_name, hospital_blockchain_address,
                                           hospital_code).create_entry()])
send_bundle(organization_bundle)
print(f"PREPARE AND SENDING LOCATION {datetime.now()}")
locations_bundle = Bundle(BundleType.Batch,
                             [Location(station=station,hospital_blockchain_address=hospital_blockchain_address).create_entry()])
send_bundle(locations_bundle)

print(f"SENDING PRACTITIONERS {datetime.now()}")
practitioners_bundle = Bundle(BundleType.Batch, [doctor.create_entry()])
send_bundle(practitioners_bundle)

patients: dict[str, Patient] = dict()
encounters: dict[str, list[EncounterDispensing]] = dict()
medicationDispenses: dict[str, list[MedicationDispense]] = dict()

print(f"PREPARE PRACTITIONERS + PATIENT + ENCOUNTER + MEDICAL DISPENSING {datetime.now()}")

for pid in range(1,10):
    patient = Patient(combine_name_surname="TEST TEST",
                      personal_id=f"cid{pid}",
                      hospital_number=f"hn{pid}",
                      hospital_blockchain_address=hospital_blockchain_address,
                      hospital_code=hospital_code)
    patients[pid] = patient
    encounters[pid] = list()
    medicationDispenses[pid] = list()
    for end in range(1,11):
        pd = ""
        dd = "2022-01-03"
        encounter = EncounterDispensing(disp_id=f"disp_id{end}",
                                        presc_date="2022-01-01", disp_date=dd,
                                        disp_status="1",
                                        belonged_to_hospital_number=f"hn{pid}",
                                        practitioner_system=doctor.license_system.system,
                                        practitioner_license_number_part=doctor.license_number_part,
                                        hospital_code=hospital_code,
                                        hospital_blockchain_address=hospital_blockchain_address)
        encounters[pid].append(encounter)
        for d in range (1,11):
            medicationDispense = MedicationDispense(disp_id=f"disp_id{end}",
                                                    disp_status="1",
                                                    local_drug_id=f"drug{d}",
                                                    standard_drug_id=f"drug{d}",
                                                    product_cat="MG",
                                                    disp_date=dd,
                                                    dfs="1234",
                                                    quantity="10",
                                                    package_size="10",
                                                    instruction_text="Eat it",
                                                    instruction_code="347",
                                                    belonged_to_hospital_number=f"hn{pid}",
                                                    hospital_code=hospital_code,
                                                    hospital_blockchain_address=hospital_blockchain_address)
            medicationDispenses[pid].append(medicationDispense)
max_patient_per_cycle = 200
cycle = 0
cycle_entries = list()
patients_count = len(patients.keys())
mode = 1
if mode == 1:
    print( f"SENDING PATIENT {datetime.now()}")
    b = [patient.create_entry() for patient in patients.values()]
    print(f"{len(b)} entries")
    send_bundle(Bundle(BundleType.Batch, b))
    print(f"SENDING ENCOUNTER {datetime.now()}")
    b= [encounter.create_entry() for e in encounters.values() for encounter in e]
    print(f"{len(b)} entries")
    send_bundle(Bundle(BundleType.Batch, b))
    print( f"SENDING MEDICAL DISPENSING {datetime.now()}")
    b = [encounter.create_entry() for e in medicationDispenses.values() for encounter in e]
    print(f"{len(b)} entries")
    send_bundle(
        Bundle(BundleType.Batch, b))
if mode == 2:
    print(
        f"SENDING PATIENT + ENCOUNTER + MEDICAL DISPENSING IN {math.ceil(patients_count / max_patient_per_cycle)} CYCLES {datetime.now()}")
    for i, key in enumerate(patients.keys()):
        cycle_entries = cycle_entries + [patients[key].create_entry()]
        if key in encounters:
            cycle_entries = cycle_entries + [encounter.create_entry() for encounter in encounters[key]]
        if key in medicationDispenses:
            cycle_entries = cycle_entries + [medication_dispense.create_entry() for medication_dispense in
                                             medicationDispenses[key]]
        if ((i > 0) and (i % max_patient_per_cycle == 0)) or (i + 1 == patients_count):
            print(f"SENDING PATIENT + ENCOUNTER + MEDICAL DISPENSING CYCLE {cycle + 1} {datetime.now()}")
            print(f"{len(cycle_entries)} entries")
            send_bundle(Bundle(BundleType.Transaction, cycle_entries))
            cycle = cycle + 1
            cycle_entries.clear()
print(f"DONE {datetime.now()}")