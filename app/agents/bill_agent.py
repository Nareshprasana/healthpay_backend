import json
import re
from app.utils.helpers import clean_json_response
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))

async def process_bill_document(text: str) -> dict:
    prompt = f"""
    Extract the following details from this medical bill:

    - Hospital name
    - Total amount (numeric only)
    - Date of service (in YYYY-MM-DD format)

    Return a JSON like this:
    {{
      "type": "bill",
      "hospital_name": "...",
      "total_amount": 1234,
      "date_of_service": "YYYY-MM-DD"
    }}

    Text:
    """
    prompt += text[:2000]

    response = client.chat.completions.create(
        model="openrouter/deepseek/deepseek-coder:free",
        messages=[
            {"role": "system", "content": "You are a medical document parsing assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    try:
        cleaned = clean_json_response(content)
        return json.loads(cleaned)
    except Exception as e:
        return {"type": "unknown", "error": f"Bill parsing error: {str(e)}"}
