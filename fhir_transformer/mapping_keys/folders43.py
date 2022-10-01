import pandas as pd

dc24totmt_mapping = pd.read_excel("data/rath_drugitems.xlsx")[["name", "did", "sks_drug_code"]].dropna(
    axis="index").set_index("did")["sks_drug_code"].to_dict()

symptom_mapping = pd.read_excel(
    "data/symptom_mapping.xlsx", index_col=0)[["SNOMED CT", "SNOMED NAME"]].to_dict(orient="index")

criticality_mapping = {1: "low", 2: "high", 3: "high",
                       4: "high", 5: "high", 6: "high", 7: "high", 8: "high"}

verificationStatus_mapping = {1: "confirmed", 2: "confirmed",
                              3: "unconfirmed", 4: "unconfirmed", 5: "unconfirmed"}