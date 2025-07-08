import re
import json

def clean_json_response(raw: str) -> str:
    """
    Cleans an LLM-generated string and extracts valid JSON from it:
    - Removes Markdown code blocks (```json)
    - Removes block comments (/* ... */)
    - Replaces single quotes with double quotes
    - Removes trailing commas
    - Extracts first valid JSON object using regex
    """
    raw = raw.strip()

    # Remove markdown markers
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)

    # Remove C-style comments
    raw = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)

    # Replace single quotes with double quotes
    raw = raw.replace("'", '"')

    # Remove trailing commas before closing braces/brackets
    raw = re.sub(r',\s*(\]|\})', r'\1', raw)

    # Extract valid JSON
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    return match.group(0) if match else raw


def try_parse_json(text: str):
    """
    Attempts to parse a string into JSON after cleaning it.
    Returns a dict if successful, or an error-wrapped dict if failed.
    """
    try:
        cleaned = clean_json_response(text)
        return json.loads(cleaned)
    except Exception as e:
        return {
            "type": "unknown",
            "error": f"JSON parsing failed: {str(e)}",
            "raw_text": text[:1000]  # keep first 1000 chars for debugging
        }


def classify_by_filename(filename: str) -> str:
    """
    Classifies the document type based on its filename.
    """
    fname = filename.lower()
    if "bill" in fname:
        return "bill"
    elif "discharge" in fname:
        return "discharge_summary"
    else:
        return "unknown"
