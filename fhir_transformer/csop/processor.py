import math
from dataclasses import dataclass
from datetime import datetime

from fhir_transformer.FHIR.Bundle import Bundle, BundleType
from fhir_transformer.FHIR.Encounter import EncounterDispensing
from fhir_transformer.FHIR.Location import Location
from fhir_transformer.FHIR.MedicationDispense import MedicationDispense
from fhir_transformer.FHIR.Organization import Organization
from fhir_transformer.FHIR.Patient import Patient
from fhir_transformer.FHIR.Practitioner import Practitioner
from fhir_transformer.csop.xml_extractor import _open_bill_trans_xml, _open_bill_disp_xml
from fhir_transformer.fhir_transformer_config import hospital_blockchain_address, max_patient_per_cycle
from fhir_transformer.utilities.networking import send_bundle

@dataclass
class EntryResult:
    status: str
    location: str | None

@dataclass
class ResourceResult:
    resourceName: str
    entries: list[EntryResult]


def process(bill_trans_xml_path: str, bill_disp_xml_path: str):
    bill_trans_xml_data = _open_bill_trans_xml(bill_trans_xml_path)
    bill_disp_xml_data = _open_bill_disp_xml(bill_disp_xml_path)

    # region GENERATE + SEND ONE ORGANIZATION DATA
    print(f"PREPARE AND SENDING ORGANIZATION {datetime.now()}")
    organization_bundle = Bundle(BundleType.Batch,
                                 [Organization(bill_trans_xml_data.hospital_name, hospital_blockchain_address,
                                               bill_trans_xml_data.hospital_code).create_entry()])

    send_bundle(organization_bundle)
    # endregion GENERATE + SEND ONE ORGANIZATION DATA

    # region GENERATE + SEND UNIQUE LOCATION DATA
    print(f"PREPARE AND SENDING LOCATION {datetime.now()}")
    locations = dict()
    for inv_no, bill_trans_item in bill_trans_xml_data.items_dict.items():
        locations[bill_trans_item.station] = Location(station=bill_trans_item.station,
                                                      hospital_blockchain_address=hospital_blockchain_address)
    locations_bundle = Bundle(BundleType.Batch, [entry.create_entry() for entry in list(locations.values())])
    send_bundle(locations_bundle)
    # endregion GENERATE + SEND UNIQUE LOCATION DATA

    # region Generate FHIR Resource for each person
    print(f"PREPARE PRACTITIONERS + PATIENT + ENCOUNTER + MEDICAL DISPENSING {datetime.now()}")
    practitioners = dict()
    patients: dict[str, Patient] = dict()
    encounters: dict[str, list[EncounterDispensing]] = dict()
    medicationDispenses: dict[str, list[MedicationDispense]] = dict()
    for disp_id, bill_disp_item in bill_disp_xml_data.items():
        corresponding_bill_trans_item = bill_trans_xml_data.items_dict[bill_disp_item.inv_no]
        # GENERATE UNIQUE PRACTITIONER
        practitioners[bill_disp_item.license_id] = Practitioner(license_id=bill_disp_item.license_id)
        # GENERATE PATIENT
        patient = Patient(combine_name_surname=corresponding_bill_trans_item.name,
                          personal_id=corresponding_bill_trans_item.pid,
                          hospital_number=corresponding_bill_trans_item.hn,
                          hospital_blockchain_address=hospital_blockchain_address,
                          hospital_code=bill_trans_xml_data.hospital_code,
                          member_number=corresponding_bill_trans_item.member_no)
        patients[corresponding_bill_trans_item.pid] = patient
        encounters[corresponding_bill_trans_item.pid] = list()
        medicationDispenses[corresponding_bill_trans_item.pid] = list()
        for bill_disp_item_detail in bill_disp_item.items:
            encounter = EncounterDispensing(disp_id=bill_disp_item_detail.disp_id,
                                            presc_date=bill_disp_item.presc_date, disp_date=bill_disp_item.disp_date,
                                            disp_status=bill_disp_item.disp_status,
                                            belonged_to_hospital_number=corresponding_bill_trans_item.hn,
                                            practitioner_system=practitioners[
                                                bill_disp_item.license_id].license_system.system,
                                            practitioner_license_number_part=practitioners[
                                                bill_disp_item.license_id].license_number_part,
                                            hospital_code=bill_trans_xml_data.hospital_code,
                                            hospital_blockchain_address=hospital_blockchain_address)
            encounters[corresponding_bill_trans_item.pid].append(encounter)
            medicationDispense = MedicationDispense(disp_id=bill_disp_item_detail.disp_id,
                                                    disp_status=bill_disp_item.disp_status,
                                                    local_drug_id=bill_disp_item_detail.local_drug_id,
                                                    standard_drug_id=bill_disp_item_detail.standard_drug_id,
                                                    product_cat=bill_disp_item_detail.product_cat,
                                                    disp_date=bill_disp_item.disp_date,
                                                    dfs=bill_disp_item_detail.dfs,
                                                    quantity=bill_disp_item_detail.quantity,
                                                    package_size=bill_disp_item_detail.package_size,
                                                    instruction_text=bill_disp_item_detail.instruction_text,
                                                    instruction_code=bill_disp_item_detail.instruction_code,
                                                    belonged_to_hospital_number=corresponding_bill_trans_item.hn,
                                                    hospital_code=bill_trans_xml_data.hospital_code,
                                                    hospital_blockchain_address=hospital_blockchain_address)
            medicationDispenses[corresponding_bill_trans_item.pid].append(medicationDispense)
    # SEND PRACTITIONERS
    print(f"SENDING PRACTITIONERS {datetime.now()}")
    practitioners_bundle = Bundle(BundleType.Batch, [entry.create_entry() for entry in list(practitioners.values())])
    send_bundle(practitioners_bundle)
    # PREPARE PATIENT + ENCOUNTER + MEDICAL DISPENSING
    cycle = 0
    cycle_entries = list()
    patients_count = len(patients.keys())
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
            send_bundle(Bundle(BundleType.Transaction, cycle_entries))
            cycle = cycle + 1
            cycle_entries.clear()
    # endregion
