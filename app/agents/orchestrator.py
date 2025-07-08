from typing import List
from fastapi import UploadFile
from app.agents.extractor import extract_text
from app.utils.helpers import classify_by_filename

async def process_claim_documents(files: List[UploadFile]) -> dict:
    documents = []

    for file in files:
        content = await file.read()
        structured_doc = await extract_text(content)

        # Safety fallback: If raw_text still returned or invalid JSON, wrap as unknown
        if not isinstance(structured_doc, dict):
            structured_doc = {
                "type": "unknown",
                "raw_text": content.decode("utf-8", errors="ignore")
            }

        # Add type if missing
        if "type" not in structured_doc:
            structured_doc["type"] = classify_by_filename(file.filename)

        documents.append(structured_doc)

    # --- Validation ---
    required_types = {"bill", "discharge_summary"}
    found_types = {doc.get("type") for doc in documents}
    missing = list(required_types - found_types)

    # --- Claim Decision ---
    if missing:
        decision = {
            "status": "rejected",
            "reason": f"Missing documents: {', '.join(missing)}"
        }
    else:
        decision = {
            "status": "approved",
            "reason": "All required documents present and data is consistent"
        }

    return {
        "documents": documents,
        "validation": {
            "missing_documents": missing,
            "discrepancies": []  # Optional: add real logic
        },
        "claim_decision": decision
    }
