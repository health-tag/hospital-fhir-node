class FHIRResource:
    resourceType: str

    def __init__(self, resource_type: str):
        self.resourceType = resource_type


class Entry:
    fullUrl: str
    resource: FHIRResource
    request = None

    def __init__(self, full_url: str, resource: FHIRResource):
        self.fullUrl = full_url
        self.resource = resource

    @classmethod
    def create_organization_entry(cls, hospital_blockchain_address: str, hospital_name: str, hospital_code: str):
        entry = cls(f"urn:uuid:Organization/{hospital_blockchain_address}", Organization(hospital_name, hospital_code))
        entry.request = {
            "method": "PUT",
            "url": f"Organization/{hospital_blockchain_address}",
            "ifNoneExist": f"identifier=https://bps.moph.go.th/hcode/5|{hospital_code}"
        }
        return entry

    @classmethod
    def create_patient_entry(cls, name: str, surname: str, thai_citizen_id: str, hospital_number: str,
                             hospital_blockchain_address: str, hospital_code: str):
        entry = cls(f"urn:uuid:Patient/{hospital_code}/{hospital_number}", Patient(name=name, surname=surname,
                                                                                   thai_citizen_id=thai_citizen_id,
                                                                                   hospital_number=hospital_number,
                                                                                   hospital_blockchain_address=hospital_blockchain_address,
                                                                                   hospital_code=hospital_code))
        entry.request = {
            "method": "PUT",
            "url": f"Patient?identifier=https://sil-th.org/CSOP/hn|{hospital_number}",
            "ifNoneExist": f"identifier=https://sil-th.org/CSOP/hn|{hospital_number}"
        }
        return entry


class Organization(FHIRResource):
    name: str
    identifier = None

    def __init__(self, hospital_name: str, hospital_code: str):
        super(Organization, self).__init__(resource_type="Organization")
        self.name = f"{hospital_name}"
        self.identifier = [
            {
                "system": "https://bps.moph.go.th/hcode/5",
                "value": f"{hospital_code}"
            }
        ]


class Patient(FHIRResource):
    name = None
    identifier = None
    generalPractitioner = None
    managingOrganization = None

    def __init__(self, name: str, surname: str, thai_citizen_id: str, hospital_number: str,
                 hospital_blockchain_address: str, hospital_code: str):
        super(Patient, self).__init__(resource_type="Patient")
        self.name = [
            {
                "use": "official",
                # "text": f"{name} {surname}",
                "family": surname,
                "given": [
                    name
                ]
            }
        ]
        self.identifier = [
            {
                "system": "https://www.dopa.go.th",
                "value": f"{thai_citizen_id}"
            },
            {
                "system": "https://sil-th.org/CSOP/hn",
                "value": f"{hospital_number}"
            }
        ]
        self.generalPractitioner = [
            {
                "type": "Organization",
                "identifier": {
                    "system": "https://bps.moph.go.th/hcode/5",
                    "value": f"{hospital_code}"
                }
            }
        ]
        self.managingOrganization = {
            "reference": f"Organization/{hospital_blockchain_address}"
        }
