from datetime import datetime

from fhir_transformer.FHIR.Bundle import Bundle, BundleType
from fhir_transformer.FHIR.Location import Location
from fhir_transformer.FHIR.Organization import Organization
from fhir_transformer.fhir_transformer_config import hospital_name_43folders, hospital_blockchain_address
from fhir_transformer.folders43.csv_extractor import _open_person_csv
from fhir_transformer.utilities.networking import send_bundle

def process(person_csv_path: str):
    personCSV = _open_person_csv(person_csv_path)
    # region GENERATE + SEND ONE ORGANIZATION DATA
    print(f"PREPARE AND SENDING ORGANIZATION {datetime.now()}")
    organization_bundle = Bundle(BundleType.Batch,
                                 [Organization(hospital_name_43folders, hospital_blockchain_address,
                                               personCSV.hospital_code).create_entry()])
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