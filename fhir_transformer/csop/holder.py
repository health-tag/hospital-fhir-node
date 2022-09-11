from dataclasses import dataclass


@dataclass
class BillTransItem:
    station: str
    inv_no: str
    hn: str
    member_no: str
    pid: str
    name: str
    pay_plan: str


@dataclass
class BillTrans:
    hospital_code: str
    hospital_name: str
    items_dict: dict[str, BillTransItem]


@dataclass
class DispensingItemDetail:
    disp_id: str
    product_cat: str
    local_drug_id: str
    standard_drug_id: str
    dfs: str
    package_size: str
    instruction_code: str
    instruction_text: str
    quantity: str
    # 'prd_code': item_split[14],
    # 'multiple_disp': item_split[17],
    # 'supply_for': item_split[18],


class DispensingItem:
    #_practitioner: str

    # @property
    # def practitioner(self):
    #    return license_mapping[self._practitioner]

    def __init__(self, provider_id: str, disp_id: str, inv_no: str, presc_date: str, disp_date: str, license_id: str,
                 disp_status: str, items: list[DispensingItemDetail]):
        self.items = items
        # self._practitioner = practitioner
        self.disp_status = disp_status
        self.license_id = license_id
        self.disp_date = disp_date
        self.presc_date = presc_date
        self.inv_no = inv_no
        self.disp_id = disp_id
        self.provider_id = provider_id
