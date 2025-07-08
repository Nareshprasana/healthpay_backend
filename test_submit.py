import requests

# Update this if your server is running on a different port or URL
url = "http://127.0.0.1:8000/process-claim"

# Files to upload – replace these with actual PDF paths on your system
files = [
    ('files', ('bill.pdf', open('sample_docs/bill.pdf', 'rb'), 'application/pdf')),
    ('files', ('discharge_summary.pdf', open('sample_docs/discharge_summary.pdf', 'rb'), 'application/pdf')),
]

response = requests.post(url, files=files)

print("Status:", response.status_code)
print("Response JSON:\n", response.json())
