from dataclasses import dataclass

from fhir_transformer.FHIR.Base import FHIRResource
from fhir_transformer.FHIR.Entry import Entry


@dataclass
class LicenseMapping:
    type: str
    system: str


license_mapping = {
    'ว': LicenseMapping(
        type='MD',
        system='https://www.tmc.or.th'
    ),
    'ท': LicenseMapping(
        type='DDS',
        system='https://www.dentalcouncil.or.th'
    ),
    'พ': LicenseMapping(
        type='NP',
        system='https://www.tnmc.or.th'
    ),
    'ภ': LicenseMapping(
        type='RPH',
        system='https://www.pharmacycouncil.org'
    )
}


class Practitioner(FHIRResource):
    _license_id: str

    def __init__(self, license_id: str):
        super(Practitioner, self).__init__(resource_type="Practitioner")
        self._license_id = license_id

    def create_entry(self) -> Entry:
        entry = Entry(f"Practitioner?identifier={self.license_system.system}|{self.license_number_part}", self, {
            "method": "PUT",
            "url": f"Practitioner?identifier={self.license_system.system}|{self.license_number_part}",
            "ifNoneExist": f"identifier={self.license_system.system}|{self.license_number_part}"
        })
        return entry

    def __getstate__(self):
        json_dict = super().__getstate__()
        del json_dict["license_system"]
        del json_dict["license_number_part"]
        return json_dict

    @property
    def text(self) -> dict[str, str]:
        return {
            "status": "extensions",
            "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{self._license_id}</div>"
        }

    @property
    def license_number_part(self) -> str:
        return self._license_id[1:]

    @property
    def license_system(self) -> LicenseMapping:
        prefix = self._license_id[0:1]
        return license_mapping[prefix]

    @property
    def identifier(self) -> list[dict[str, str | dict[str, str]]]:
        return [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": f"{self.license_system.type}"
                        }
                    ]
                },
                "system": f"{self.license_system.system}",
                "value": f"{self.license_number_part}"
            }
        ]
