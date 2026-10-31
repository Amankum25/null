import csv
import json
import os

CATEGORY_MAP = {
    "identity-certificates": "certificates",
    "birth-death-marriage": "certificates",
    "education-scholarships": "education",
    "transport-vehicles": "licenses",
    "business-licences": "licenses",
    "pension-welfare": "benefits",
    "ration-food": "benefits",
    "agriculture-rural": "benefits",
    "labour-employment": "benefits",
    "land-property-revenue": "registrations",
    "utilities-municipal": "registrations",
    "grievance-rti": "other",
}

DOC_PRESETS = {
    "certificates": ["Aadhaar Card", "Proof of Address (Electricity Bill / Ration Card)", "Self-Declaration / Affidavit", "Age Proof"],
    "education": ["Aadhaar Card", "Admission Letter / College ID", "Previous Year Marksheet", "Income Certificate", "Bank Passbook"],
    "licenses": ["Aadhaar / Voter ID", "Proof of Address", "Age Proof / Physical Fitness Certificate", "Photographs"],
    "benefits": ["Aadhaar Card", "Bank Account Details / Passbook", "Income Certificate / BPL Card", "Category Proof"],
    "registrations": ["Property Deed / Electricity Bill", "Aadhaar Card", "PAN Card", "Passport Photographs"],
    "other": ["Aadhaar Card", "Grievance / Request Application Letter", "Supporting Documents"],
}

csv_path = os.path.join("CivicFlow_India_Service_Inventory_Important_Files_v1", "national_service_seed_matrix.csv")

records = []
with open(csv_path, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        state_code = row["state_code"].strip()
        raw_sid = row["service_id"].strip().replace("_", "-")
        sid = f"{state_code.lower()}-{raw_sid}"
        title = row["service_name"].strip()
        state_name = row["state_or_ut"].strip()
        cat_raw = row["category_id"].strip()
        cat = CATEGORY_MAP.get(cat_raw, "other")
        dept = row["department_hint"].strip().replace(" | ", " & ")
        url = row["primary_portal_url"].strip()
        note = row["note"].strip()

        desc = f"Official {title} service for citizens in {state_name}. Apply through the state government portal."
        docs = DOC_PRESETS.get(cat, ["Aadhaar Card", "Proof of Identity", "Proof of Address"])

        records.append({
            "id": sid,
            "title": f"{title} ({state_name})",
            "category": cat,
            "description": desc,
            "jurisdiction": state_name,
            "state_code": state_code,
            "department": dept or f"{state_name} State Department",
            "officialUrl": url,
            "status": "available",
            "integrationMode": "civicflow_assisted",
            "workflowSteps": ["Service Requirements", "Citizen Profile", "Document Verification", "Portal Access", "Form Review & Submission"],
            "eligibility": [f"Resident of {state_name}", "Valid Aadhaar / Identity proof", "Fulfillment of department guidelines"],
            "documents": docs,
            "aliases": [title, f"{title} {state_name}", state_code, raw_sid.replace("-", " ")],
        })

print(f"Loaded {len(records)} records from CSV.")
with open("src/data/seedServices.json", "w", encoding="utf-8") as out:
    json.dump(records, out, indent=2, ensure_ascii=False)
print("Wrote src/data/seedServices.json successfully!")

