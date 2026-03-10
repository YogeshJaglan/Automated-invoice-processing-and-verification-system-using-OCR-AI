# from pathlib import Path
# import json
# import re

# BASE_DIR = Path(__file__).resolve().parents[2]

# OCR_FILE = BASE_DIR / "output" / "extracted_text" / "invoice_text.txt"

# OUTPUT_DIR = BASE_DIR / "output" / "structured_data"
# OUTPUT_FILE = OUTPUT_DIR / "final_invoice.json"

# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# # -------------------------------------------------
# # LOAD OCR TEXT
# # -------------------------------------------------

# def load_ocr_text():

#     if not OCR_FILE.exists():
#         raise FileNotFoundError("OCR text file not found")

#     return OCR_FILE.read_text(encoding="utf-8")


# # -------------------------------------------------
# # GSTIN EXTRACTION
# # -------------------------------------------------

# def extract_gstin(text):

#     text = text.upper()

#     pattern = r"\b\d{2}[A-Z]{5}\d{4}[A-Z]\d[A-Z0-9]\d\b"

#     matches = re.findall(pattern, text)

#     if matches:
#         return matches[0]

#     return None


# # -------------------------------------------------
# # DATE
# # -------------------------------------------------

# def extract_invoice_date(text):

#     text_lower = text.lower()

#     patterns = [

#         r"invoice date[:\s]*([0-9]{2}[./-][0-9]{2}[./-][0-9]{4})",

#         r"order date[:\s]*([0-9]{2}[./-][0-9]{2}[./-][0-9]{4})",

#         r"\b([0-9]{2}\.[0-9]{2}\.[0-9]{4})\b"
#     ]

#     for p in patterns:

#         match = re.search(p, text_lower)

#         if match:
#             return match.group(1)

#     return None


# # -------------------------------------------------
# # INVOICE NUMBER
# # -------------------------------------------------

# def extract_invoice_number(text):

#     text_lower = text.lower()

#     patterns = [

#         r"invoice number[:\s]*([a-z0-9\-]+)",

#         r"\b([a-z]{2,4}\d[- ]?\d{6,})\b"
#     ]

#     for p in patterns:

#         match = re.search(p, text_lower)

#         if match:
#             return match.group(1).replace(" ", "-").upper()

#     return None


# # -------------------------------------------------
# # VENDOR DETECTION
# # -------------------------------------------------

# def extract_vendor(text):

#     lines = text.split("\n")

#     for i, line in enumerate(lines):

#         if "sold by" in line.lower():

#             for j in range(i + 1, min(i + 5, len(lines))):

#                 vendor = lines[j].strip()

#                 if len(vendor) > 4:

#                     if "amazon" in vendor.lower():
#                         continue

#                     if "address" in vendor.lower():
#                         continue

#                     return vendor.upper()

#     for i, line in enumerate(lines):

#         if "authorized signatory" in line.lower():

#             for j in range(i - 1, max(i - 5, 0), -1):

#                 vendor = lines[j].strip()

#                 if len(vendor) > 4:

#                     vendor = vendor.replace("for ", "")

#                     return vendor.upper()

#     return None


# # -------------------------------------------------
# # TOTAL AMOUNT
# # -------------------------------------------------

# def extract_total(text):

#     text_clean = text.replace(",", "")

#     text_lower = text_clean.lower()

#     patterns = [

#         r"grand total[:\s]*([0-9]+\.\d{2})",

#         r"total amount[:\s]*([0-9]+\.\d{2})",

#         r"amount payable[:\s]*([0-9]+\.\d{2})",

#         r"total[:\s]*([0-9]+\.\d{2})"
#     ]

#     for p in patterns:

#         match = re.search(p, text_lower)

#         if match:
#             return float(match.group(1))

#     numbers = re.findall(r"\d+\.\d{2}", text_clean)

#     numbers = [float(n) for n in numbers if 10 < float(n) < 500000]

#     if numbers:
#         return max(numbers)

#     return 0


# # -------------------------------------------------
# # TAX EXTRACTION
# # -------------------------------------------------

# def extract_tax(text):

#     text_lower = text.lower()

#     cgst = 0
#     sgst = 0
#     igst = 0

#     cgst_match = re.search(r"cgst.*?([0-9]+\.[0-9]+)", text_lower)
#     sgst_match = re.search(r"sgst.*?([0-9]+\.[0-9]+)", text_lower)
#     igst_match = re.search(r"igst.*?([0-9]+\.[0-9]+)", text_lower)

#     if cgst_match:
#         cgst = float(cgst_match.group(1))

#     if sgst_match:
#         sgst = float(sgst_match.group(1))

#     if igst_match:
#         igst = float(igst_match.group(1))

#     tax_type = "UNKNOWN"

#     if cgst and sgst:
#         tax_type = "CGST_SGST"

#     if igst:
#         tax_type = "IGST"

#     return {

#         "type": tax_type,

#         "cgst": cgst,

#         "sgst": sgst,

#         "igst": igst
#     }


# # -------------------------------------------------
# # BUILD JSON
# # -------------------------------------------------

# def build_invoice(text):

#     invoice = {

#         "vendor_name": extract_vendor(text),

#         "gstin": extract_gstin(text),

#         "invoice_number": extract_invoice_number(text),

#         "invoice_date": extract_invoice_date(text),

#         "total_amount": extract_total(text),

#         "tax": extract_tax(text)
#     }

#     return invoice


# # -------------------------------------------------
# # MAIN
# # -------------------------------------------------

# if __name__ == "__main__":

#     text = load_ocr_text()

#     invoice = build_invoice(text)

#     with open(OUTPUT_FILE, "w") as f:
#         json.dump(invoice, f, indent=4)

#     print("Invoice parsed successfully")

#     print(invoice)








import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

OCR_FILE = BASE_DIR / "output" / "extracted_text" / "invoice_text.txt"

OUTPUT_DIR = BASE_DIR / "output" / "structured_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "final_invoice.json"

text = OCR_FILE.read_text(encoding="utf-8")
lower = text.lower()


# -------------------------------
# Vendor Name
# -------------------------------

def extract_vendor():

    lines = text.split("\n")

    for i, line in enumerate(lines):

        if "sold by" in line.lower():

            if i + 1 < len(lines):
                return lines[i + 1].strip()

    return None


# -------------------------------
# GSTIN
# -------------------------------

def extract_gstin():

    pattern = r"\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9][A-Z0-9]\d"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# -------------------------------
# Invoice Number
# -------------------------------

def extract_invoice_number():

    patterns = [
        r"invoice number\s*[:\-]?\s*([A-Z0-9\-]+)",
        r"invoice details\s*[:\-]?\s*([A-Z0-9\-]+)"
    ]

    for p in patterns:

        match = re.search(p, lower)

        if match:
            return match.group(1)

    return None


# -------------------------------
# Invoice Date
# -------------------------------

def extract_invoice_date():

    pattern = r"\d{2}[./]\d{2}[./]\d{4}"

    matches = re.findall(pattern, text)

    if matches:
        return matches[0]

    return None


# -------------------------------
# Total Amount
# -------------------------------

def extract_total_amount():

    numbers = re.findall(r"\d+\.\d{2}", text)

    if numbers:

        nums = [float(n) for n in numbers]

        return max(nums)

    return None


invoice = {

    "vendor_name": extract_vendor(),

    "gstin": extract_gstin(),

    "invoice_number": extract_invoice_number(),

    "invoice_date": extract_invoice_date(),

    "total_amount": extract_total_amount()
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(invoice, f, indent=4)

print("\nInvoice parsed successfully\n")
print(invoice)