from pydantic import BaseModel
from typing import List, Dict, Any

class ClaimResponse(BaseModel):
    documents: List[Dict[str, Any]]
    validation: Dict[str, Any]
    claim_decision: Dict[str, Any]
