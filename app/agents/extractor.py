import os
import json
import re
import httpx
import fitz
import pdfplumber
import io
from typing import Any
from dotenv import load_dotenv
from app.utils.helpers import clean_json_response

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

# 📄 Extract text with fallback: PyMuPDF first, then pdfplumber
def extract_text_fallback(pdf_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        if text.strip():
            return text
    except Exception:
        pass

    # fallback to pdfplumber
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return f"Extraction failed: {str(e)}"


# 🧠 Main function to send prompt to OpenRouter and parse JSON
async def extract_text(content: bytes) -> dict[str, Any]:
    raw_text = extract_text_fallback(content)

    prompt = f"""Extract structured medical insurance claim data in JSON format from the following text:
\"\"\"
{raw_text[:2000]}
\"\"\"
Only return valid, parsable JSON. Avoid code blocks or markdown formatting.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",  # Replace with actual in prod
        "X-Title": "healthpay-claim-parser"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful insurance claim document parser."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )

        response.raise_for_status()
        ai_response = response.json()
        raw_result = ai_response["choices"][0]["message"]["content"]
        cleaned = clean_json_response(raw_result)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Retry with basic sanitization
            sanitized = cleaned.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
            try:
                return json.loads(sanitized)
            except Exception as e:
                raise ValueError(f"Sanitized JSON still failed: {str(e)}")

    except Exception as e:
        return {
            "documents": [{"error": f"Unexpected error: {str(e)}", "type": "unknown"}],
            "validation": {
                "missing_documents": ["bill", "discharge_summary"],
                "discrepancies": []
            },
            "claim_decision": {
                "status": "rejected",
                "reason": "Missing documents: bill, discharge_summary"
            }
        }
