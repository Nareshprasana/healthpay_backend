# app/agents/decision_agent.py

async def decide_claim(documents: list, validation: dict) -> dict:
    if validation["missing_documents"]:
        return {
            "status": "rejected",
            "reason": f"Missing documents: {', '.join(validation['missing_documents'])}"
        }
    return {
        "status": "approved",
        "reason": "All required documents present and data is consistent"
    }
