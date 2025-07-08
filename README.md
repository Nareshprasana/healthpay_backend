Great! Below is the complete production-ready version of your `README.md` and `Dockerfile` to complete your HealthPay backend assignment.

---

### 📄 `README.md`

```
# HealthPay - Claim Document Processor (Backend)

A FastAPI-based backend system that processes medical insurance claim documents using AI-powered agentic workflows.

## ✅ Features

- Accepts multiple medical documents (PDFs) via `/process-claim` endpoint
- Extracts and classifies documents using LLMs (via OpenRouter)
- Validates required documents: `bill`, `discharge_summary`
- Approves or rejects claims with reasons
- Modular & testable code structure
- Fully async and production-ready

---

## 🛠️ Tech Stack

- **FastAPI**: Web framework
- **httpx**: Async HTTP client
- **PyMuPDF**: PDF parsing
- **OpenRouter + DeepSeek**: LLM-based document processing
- **dotenv**: Secure API key loading

---

## 📦 Folder Structure

```

app/
│
├── main.py                         # FastAPI app entrypoint
│
├── agents/
│   ├── extractor.py               # Extracts & calls LLM
│   └── orchestrator.py           # Controls workflow logic
│
└── utils/
└── helpers.py                # Utility functions

````

---

## 🚀 Running Locally

### 1. Clone & install dependencies:

```bash
git clone https://github.com/your-username/healthpay-backend.git
cd healthpay-backend
pip install -r requirements.txt
````

### 2. Setup `.env` file:

Create a file `.env` in the root directory:

```
OPENROUTER_API_KEY=your_openrouter_key_here
```

### 3. Start the server:

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for Swagger UI.

---

## 🧪 Example API Usage

**POST** `/process-claim`
**Content-Type:** `multipart/form-data`
**Files:** Upload multiple PDF files

**Sample JSON Output:**

```json
{
  "documents": [
    {
      "type": "bill",
      "hospital_name": "XYZ Hospital",
      "total_amount": 25000,
      "date_of_service": "2025-02-01"
    },
    {
      "type": "discharge_summary",
      "patient_name": "John Doe",
      "diagnosis": "Fracture",
      "admission_date": "2025-01-30",
      "discharge_date": "2025-02-02"
    }
  ],
  "validation": {
    "missing_documents": [],
    "discrepancies": []
  },
  "claim_decision": {
    "status": "approved",
    "reason": "All required documents present and data is consistent"
  }
}
```

---

## 🤖 AI Tools Used

* **Cursor AI**: Prompt debugging, refactoring
* **ChatGPT (GPT-4)**: Code architecture, LLM prompt design
* **DeepSeek (OpenRouter)**: Free LLM used for structured document extraction

---

## 💬 Sample Prompts

> 🧠 Prompt 1 (Extraction):

```
Extract structured medical information in JSON format from the following discharge summary. Return only valid JSON.
```

> 🧠 Prompt 2 (Validation):

```
Check if the total bill amount matches the sum of line items. Flag inconsistencies.
```

> 🧠 Prompt 3 (Classification):

```
Based on filename and content, classify if this is a 'bill', 'discharge_summary', or 'unknown'.
```

---

## 🐳 Docker Support (Optional)

You can also run the project via Docker (see Dockerfile below).

---

## 🏁 Final Note

This project was built as part of the **HealthPay Backend Developer Assignment** to demonstrate:

* Modular backend design
* AI-powered document processing
* Practical agent orchestration

````

---

### 🐳 `Dockerfile`

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
````
