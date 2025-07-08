# app/agents/discharge_agent.py

def process_discharge_document(text: str) -> dict:
    # In real use-case, you'd parse based on patterns, NER, or use an LLM.
    from datetime import datetime
    import re

    def extract_field(field_label):
        match = re.search(rf"{field_label}:?\s*(.*)", text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    return {
        "type": "discharge_summary",
        "patient_name": extract_field("Patient Name"),
        "diagnosis": extract_field("Diagnosis"),
        "admission_date": extract_field("Admission Date"),
        "discharge_date": extract_field("Discharge Date"),
    }


def process_bill_document(text: str) -> dict:
    import re

    def extract_field(field_label):
        match = re.search(rf"{field_label}:?\s*(.*)", text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def extract_amount():
        match = re.search(r'Total Amount.*?([\d,]+\.\d{2})', text)
        if match:
            return float(match.group(1).replace(',', ''))
        return None

    return {
        "type": "bill",
        "hospital_name": extract_field("Hospital Name"),
        "total_amount": extract_amount(),
        "date_of_service": extract_field("Date of Service") or extract_field("Billing Date"),
    }
