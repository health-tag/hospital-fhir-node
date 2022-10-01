from dataclasses import dataclass

@dataclass
class PersonItem:
    cid: str
    pid: str
    hn: str
    name: str
    surname: str
    gender: str

@dataclass
class PersonCSV:
    hospital_code: str
    items_dict: dict[str, PersonItem]

@dataclass
class DrugItem:
    pid: str
    sequence: str
    date_service:str
    clinic: str
    drug_id: str
    dung_name: str
    amount: str
    unit: str
    unit_packing: str
    provider_id: str
    cid: str

@dataclass
class ProviderItem:
    provider_id: str
    register_no: str
    council:str
    cid: str
    title: str
    name: str
    surname: str
    gender: str
