from abc import abstractmethod
from typing import Dict, Any


class FHIRResource:
    resourceType: str

    def __init__(self, resource_type: str):
        self.resourceType = resource_type

    @abstractmethod
    def __getstate__(self) -> dict[str, Any]:
        json_dict = self.__dict__.copy()
        keys_to_be_deleted = [key for key in json_dict if key.startswith("_")]
        for key in keys_to_be_deleted:
            del json_dict[key]
        return json_dict
