# app/agents/validation.py

def validate_documents(docs: list[dict]) -> dict:
    required_types = {"bill", "discharge_summary"}
    found_types = {doc.get("type") for doc in docs}

    missing_documents = list(required_types - found_types)
    discrepancies = []

    for doc in docs:
        for key, value in doc.items():
            if value is None or value == "":
                discrepancies.append(f"Missing value for '{key}' in {doc.get('type')}")

    return {
        "missing_documents": missing_documents,
        "discrepancies": discrepancies
    }
