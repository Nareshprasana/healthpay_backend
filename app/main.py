from fastapi import FastAPI, UploadFile, File
from typing import List
from app.agents.orchestrator import process_claim_documents

app = FastAPI()

@app.post("/process-claim")
async def process_claim(files: List[UploadFile] = File(...)):
    return await process_claim_documents(files)
