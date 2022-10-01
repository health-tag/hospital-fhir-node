import pandas as pd

from fhir_transformer.folders43.holders import PersonItem, PersonCSV, ProviderItem, DrugItem


def _open_person_csv(file_path: str) -> PersonCSV:
    # HOSPCODE|CID|PID|HID|PRENAME|NAME|LNAME|HN|SEX|BIRTH|MSTATUS|OCCUPATION_OLD|OCCUPATION_NEW|RACE|NATION|RELIGION|EDUCATION|FSTATUS|FATHER|MOTHER|COUPLE|VSTATUS|MOVEIN|DISCHARGE|DDISCHARGE|ABOGROUP|RHGROUP|LABOR|PASSPORT|TYPEAREA|D_UPDATE|TELEPHONE|MOBILE
    df = pd.read_csv(file_path, encoding="utf8", delimiter="|")
    item_dict = dict[str, PersonItem]()
    hoscode = 0
    for i, row in df.iterrows():
        hoscode = row["HOSCODE"]
        item_dict[row["pid"]] = PersonItem(cid=row["CID"], pid=row["PID"], hn=row["HN"], name=row["NAME"],
                                           surname=row["LNAME"], gender=row["SEX"])
    return PersonCSV(hospital_code=hoscode, items_dict=item_dict)


def _open_provider_csv(file_path: str) -> dict[str, ProviderItem]:
    # HOSPCODE|PROVIDER|REGISTERNO|COUNCIL|CID|PRENAME|NAME|LNAME|SEX|BIRTH|PROVIDERTYPE|STARTDATE|OUTDATE|MOVEFROM|MOVETO|D_UPDATE
    df = pd.read_csv(file_path, encoding="utf8", delimiter="|")
    item_dict = dict[str, ProviderItem]()
    for i, row in df.iterrows():
        item_dict[row["PROVIDER"]] = ProviderItem(provider_id=row["PROVIDER"], register_no=row["REGISTERNO"],
                                                  council=row["COUNCIL"],
                                                  cid=row["CID"], name=row["NAME"], surname=row["LNAME"],
                                                  gender=row["SEX"])
    return item_dict


def _open_drug_opd_csv(file_path: str) -> dict[str, DrugItem]:
    # HOSPCODE|PID|SEQ|DATE_SERV|CLINIC|DIDSTD|DNAME|AMOUNT|UNIT|UNIT_PACKING|DRUGPRICE|DRUGCOST|PROVIDER|D_UPDATE|CID
    df = pd.read_csv(file_path, encoding="utf8", delimiter="|")
    item_dict = dict[str, DrugItem]()
    for i, row in df.iterrows():
        item_dict[row["pid"]] = DrugItem(cid=row["CID"], pid=row["PID"], sequence=row["SEQ"],
                                         date_service=row["DATE_SERV"],
                                         clinic=row["CLINIC"], drug_id=row["DIDSTD"], dung_name=row["DNAME"],
                                         amount=row["AMOUNT"], unit=row["UNIT"], unit_packing=row["UNIT_PACKING"],
                                         provider_id=row["PROVIDER"])
    return item_dict
