import json
import requests
from faker import Faker

fake = Faker()
data = []

for i in range(5000):
    permission = 1 if i < 250 else 2
    ms_id = f"A-{i + 1:05}" if permission == 1 else f"B-{i - 249:05}"
    name = fake.name()
    data.append({
        "name": name,
        "ms_id": ms_id,
        "pwd": "0000",
        "permissions": permission
    })

print(data)

with open("Medical_Staff.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# drug_data = []

# api_url = "https://api.fda.gov/drug/label.json?limit=1000"

# response = requests.get(api_url)
# if response.status_code == 200:
#     data = response.json()
#     medications = data.get("results", [])
# else:
#     medications = []
#     print("API request failed!")

# for medicationn_data in medications:
#     drug_class = medicationn_data.get("openfda", {}).get("route", [None])[0]
#     if not medicationn_data.get("openfda", {}).get("brand_name", [None])[0]:
#         continue
#     if drug_class == "INTRAMUSCULAR" or drug_class == "INTRATHECAL" or drug_class == "EPIDURAL" or drug_class == "INTRAVENOUS" or drug_class == "SUBCUTANEOUS":
#         drug_class = 0
#     elif drug_class == "ORAL":
#         drug_class = 1
#     elif drug_class == "OPHTHALMIC" or drug_class == "CUTANEOUS" or drug_class == "TRANSDERMAL" or drug_class == "DENTAL" or drug_class == "RESPIRATORY (INHALATION)" or drug_class == "NASAL" or drug_class == "TOPICAL" or drug_class == "VAGINAL" or drug_class == "IRRIGATION":
#         drug_class = 2
#     else:
#         drug_class = 3
#     drug_data.append({
#         "name": medicationn_data.get("openfda", {}).get("brand_name", [None])[0],
#         "effect": medicationn_data.get("purpose", [None])[0],
#         "side_effect": medicationn_data.get("warnings", [None])[0],
#         "drug_class": drug_class
#     })

# print(drug_data)

# with open("Medication.json", "w", encoding="utf-8") as f:
#     json.dump(drug_data, f, ensure_ascii=False, indent=4)