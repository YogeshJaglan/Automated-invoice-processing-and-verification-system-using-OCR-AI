# import requests
# import json
# from pathlib import Path

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# OCR_FILE = BASE_DIR / "output" / "extracted_text" / "invoice_text.txt"
# OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"

# OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# # -------------------------------------------------
# # READ OCR TEXT
# # -------------------------------------------------

# text = OCR_FILE.read_text(encoding="utf-8")

# # -------------------------------------------------
# # PROMPT
# # -------------------------------------------------

# prompt = f"""
# Extract the following fields from the invoice text.

# Return ONLY JSON.

# Fields:
# vendor_name
# gstin
# invoice_number
# invoice_date
# total_amount

# Invoice text:
# {text}
# """

# # -------------------------------------------------
# # OLLAMA REQUEST
# # -------------------------------------------------

# url = "http://localhost:11434/api/generate"

# payload = {
#     "model": "llama3.2",
#     "prompt": prompt,
#     "stream": False
# }

# response = requests.post(url, json=payload)

# data = response.json()

# # -------------------------------------------------
# # SAFE RESPONSE HANDLING
# # -------------------------------------------------

# if "response" not in data:

#     print("❌ Ollama response error:")
#     print(data)

#     result_text = "{}"

# else:

#     result_text = data["response"]

# # -------------------------------------------------
# # CLEAN JSON OUTPUT
# # -------------------------------------------------

# result_text = result_text.strip()

# if "```json" in result_text:
#     result_text = result_text.split("```json")[1].split("```")[0]

# if "```" in result_text:
#     result_text = result_text.replace("```", "")

# try:

#     parsed = json.loads(result_text)

# except:

#     parsed = {
#         "vendor_name": None,
#         "gstin": None,
#         "invoice_number": None,
#         "invoice_date": None,
#         "total_amount": None
#     }

# # -------------------------------------------------
# # SAVE RESULT
# # -------------------------------------------------

# OUTPUT_FILE.write_text(json.dumps(parsed, indent=4))

# print("AI extraction completed")
# print("Saved to:", OUTPUT_FILE)









# import requests
# import json
# import re
# from pathlib import Path

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# OCR_FILE = BASE_DIR / "output" / "extracted_text" / "invoice_text.txt"
# OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"

# OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# # -------------------------------------------------
# # READ OCR TEXT
# # -------------------------------------------------

# text = OCR_FILE.read_text(encoding="utf-8")

# # -------------------------------------------------
# # PROMPT
# # -------------------------------------------------

# prompt = f"""
# Extract the following fields from the invoice text.

# Return ONLY JSON.

# Fields:
# vendor_name
# gstin
# invoice_number
# invoice_date
# total_amount

# Invoice text:
# {text}
# """

# # -------------------------------------------------
# # OLLAMA REQUEST
# # -------------------------------------------------

# url = "http://localhost:11434/api/generate"

# payload = {
#     "model": "llama3.2",
#     "prompt": prompt,
#     "stream": False
# }

# response = requests.post(url, json=payload)
# data = response.json()

# # -------------------------------------------------
# # SAFE RESPONSE HANDLING
# # -------------------------------------------------

# if "response" not in data:
#     print("❌ Ollama response error:")
#     print(data)
#     result_text = "{}"
# else:
#     result_text = data["response"]

# # -------------------------------------------------
# # CLEAN JSON OUTPUT
# # -------------------------------------------------

# result_text = result_text.strip()

# if "```json" in result_text:
#     result_text = result_text.split("```json")[1].split("```")[0]

# if "```" in result_text:
#     result_text = result_text.replace("```", "")

# # -------------------------------------------------
# # PARSE JSON SAFELY
# # -------------------------------------------------

# try:
#     parsed = json.loads(result_text)
# except:
#     parsed = {
#         "vendor_name": None,
#         "gstin": None,
#         "invoice_number": None,
#         "invoice_date": None,
#         "total_amount": None
#     }

# # -------------------------------------------------
# # SAFE TOTAL AMOUNT CHECK (minimal fix)
# # -------------------------------------------------

# amount = parsed.get("total_amount")


# def extract_total_from_text(text):
#     matches = re.findall(r"total[^0-9]*([\d,]+\.\d+)", text.lower())
#     if matches:
#         return matches[-1].replace(",", "")
#     return None


# # Only fix if AI returned invalid value
# if amount in [None, "null", "", "None"]:
#     corrected = extract_total_from_text(text)
#     if corrected:
#         parsed["total_amount"] = corrected

# # -------------------------------------------------
# # SAVE RESULT
# # -------------------------------------------------

# OUTPUT_FILE.write_text(json.dumps(parsed, indent=4))

# print("AI extraction completed")
# print("Saved to:", OUTPUT_FILE)











import requests
import json
from pathlib import Path

# -------------------------------------------------
# PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

OCR_FILE = BASE_DIR / "output" / "extracted_text" / "invoice_text.txt"
OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# READ OCR TEXT
# -------------------------------------------------

text = OCR_FILE.read_text(encoding="utf-8")

# -------------------------------------------------
# PROMPT FOR OLLAMA
# -------------------------------------------------

prompt = f"""
Extract the following fields from the invoice text.

Return ONLY valid JSON.

Fields:
vendor_name
gstin
invoice_number
invoice_date
total_amount

Important rules:
- total_amount must be the FINAL TOTAL payable amount
- ignore unit price, tax rows, subtotal rows
- return only the final payable amount

Invoice text:
{text}
"""

# -------------------------------------------------
# OLLAMA REQUEST
# -------------------------------------------------

url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2",
    "prompt": prompt,
    "stream": False
}

response = requests.post(url, json=payload)
data = response.json()

# -------------------------------------------------
# HANDLE RESPONSE
# -------------------------------------------------

if "response" not in data:

    print("❌ Ollama response error:")
    print(data)

    result_text = "{}"

else:

    result_text = data["response"]

# -------------------------------------------------
# CLEAN JSON OUTPUT
# -------------------------------------------------

result_text = result_text.strip()

if "```json" in result_text:
    result_text = result_text.split("```json")[1].split("```")[0]

if "```" in result_text:
    result_text = result_text.replace("```", "")

# -------------------------------------------------
# PARSE JSON
# -------------------------------------------------

try:

    parsed = json.loads(result_text)

except:

    parsed = {
        "vendor_name": None,
        "gstin": None,
        "invoice_number": None,
        "invoice_date": None,
        "total_amount": None
    }

# -------------------------------------------------
# CLEAN VALUES
# -------------------------------------------------

def clean_value(value):

    if value in ["null", "None", "", None]:
        return None

    return value


parsed["vendor_name"] = clean_value(parsed.get("vendor_name"))
parsed["gstin"] = clean_value(parsed.get("gstin"))
parsed["invoice_number"] = clean_value(parsed.get("invoice_number"))
parsed["invoice_date"] = clean_value(parsed.get("invoice_date"))
parsed["total_amount"] = clean_value(parsed.get("total_amount"))

# -------------------------------------------------
# SAVE RESULT
# -------------------------------------------------

OUTPUT_FILE.write_text(json.dumps(parsed, indent=4))

print("AI extraction completed")
print("Saved to:", OUTPUT_FILE)