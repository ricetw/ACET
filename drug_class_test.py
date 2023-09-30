import json

with open("Medication.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
drug_classes = set(item["drug_class"] for item in data)

print(drug_classes)
for drug_class in drug_classes:
    print(drug_class)