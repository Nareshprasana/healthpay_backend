async def classify_document(filename: str, content: bytes) -> str:
    if "bill" in filename.lower():
        return "bill"
    elif "discharge" in filename.lower():
        return "discharge_summary"
    else:
        return "unknown"
