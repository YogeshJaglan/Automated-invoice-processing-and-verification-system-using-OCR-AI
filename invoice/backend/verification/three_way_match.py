# from pathlib import Path
# import json

# BASE_DIR = Path(__file__).resolve().parents[2]

# INVOICE_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"
# PO_FILE = BASE_DIR / "data" / "purchase_orders.json"

# OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"


# # -----------------------------
# # Load Files
# # -----------------------------

# invoice = json.loads(INVOICE_FILE.read_text())

# po_list = json.loads(PO_FILE.read_text())


# vendor = str(invoice.get("vendor_name", "")).lower()
# invoice_amount = float(invoice.get("total_amount", 0))


# status = "FLAGGED"
# reasons = []


# # -----------------------------
# # Match PO
# # -----------------------------

# match_found = False

# for po in po_list:

#     po_vendor = str(
#         po.get("vendor") or
#         po.get("vendor_name") or
#         po.get("supplier") or
#         ""
#     ).lower()

#     po_amount = float(po.get("amount", 0))

#     if po_vendor in vendor or vendor in po_vendor:

#         match_found = True

#         if abs(po_amount - invoice_amount) < 5:
#             status = "APPROVED"
#         else:
#             reasons.append("Amount mismatch with PO")

#         break


# if not match_found:
#     reasons.append("No matching Purchase Order found")


# # -----------------------------
# # Save Result
# # -----------------------------

# result = {
#     "status": status,
#     "reasons": reasons
# }

# OUTPUT_FILE.write_text(json.dumps(result, indent=4))

# print("3-WAY MATCHING COMPLETED")



























# from pathlib import Path
# import json

# BASE_DIR = Path(__file__).resolve().parents[2]

# INVOICE_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"
# PO_FILE = BASE_DIR / "data" / "purchase_orders.json"

# OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"


# # -----------------------------
# # SAFE FLOAT FUNCTION
# # -----------------------------

# def safe_float(value, default=0.0):

#     if value in [None, "null", "None", ""]:
#         return default

#     try:
#         return float(value)
#     except:
#         return default


# # -----------------------------
# # Load Files
# # -----------------------------

# invoice = json.loads(INVOICE_FILE.read_text())

# po_list = json.loads(PO_FILE.read_text())


# vendor = str(invoice.get("vendor_name", "")).lower()

# invoice_amount = safe_float(invoice.get("total_amount"))


# status = "FLAGGED"
# reasons = []


# # -----------------------------
# # Match PO
# # -----------------------------

# match_found = False

# for po in po_list:

#     po_vendor = str(
#         po.get("vendor") or
#         po.get("vendor_name") or
#         po.get("supplier") or
#         ""
#     ).lower()

#     po_amount = safe_float(po.get("total_amount"))

#     if po_vendor in vendor or vendor in po_vendor:

#         match_found = True

#         if abs(po_amount - invoice_amount) < 5:
#             status = "APPROVED"
#         else:
#             reasons.append("Amount mismatch with PO")

#         break


# if not match_found:
#     reasons.append("No matching Purchase Order found")


# # -----------------------------
# # Save Result
# # -----------------------------

# result = {
#     "status": status,
#     "reasons": reasons
# }

# OUTPUT_FILE.write_text(json.dumps(result, indent=4))

# print("3-WAY MATCHING COMPLETED")










# from pathlib import Path
# import json
# import sys

# # ✅ ADD THIS IMPORT
# from backend.database.mongo import invoices_collection

# BASE_DIR = Path(__file__).resolve().parents[2]

# INVOICE_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"
# PO_FILE = BASE_DIR / "data" / "purchase_orders.json"

# OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"


# # -----------------------------
# # SAFE FLOAT FUNCTION
# # -----------------------------
# def safe_float(value, default=0.0):
#     if value in [None, "null", "None", ""]:
#         return default

#     try:
#         return float(value)
#     except:
#         return default


# # -----------------------------
# # LOAD FILES
# # -----------------------------
# invoice = json.loads(INVOICE_FILE.read_text())
# po_list = json.loads(PO_FILE.read_text())


# # -----------------------------
# # EXTRACT INVOICE DATA
# # -----------------------------
# vendor = str(invoice.get("vendor_name", "")).lower()
# invoice_amount = safe_float(invoice.get("total_amount"))
# invoice_number = str(invoice.get("invoice_number", "")).lower()


# # -----------------------------
# # INITIAL STATUS
# # -----------------------------
# status = "FLAGGED"
# reasons = []


# # -----------------------------
# # DUPLICATE CHECK (MONGODB)
# # -----------------------------
# existing_invoice = invoices_collection.find_one({
#     "invoice_number": invoice.get("invoice_number"),
#     "vendor_name": invoice.get("vendor_name")
# })

# if existing_invoice:
#     result = {
#         "status": "REJECTED",
#         "reasons": ["Duplicate invoice detected (DB)"]
#     }

#     OUTPUT_FILE.write_text(json.dumps(result, indent=4))
#     print("❌ DUPLICATE INVOICE FOUND (DB)")

#     sys.exit()   # Stop execution completely


# # -----------------------------
# # MATCH PO (3-WAY MATCHING)
# # -----------------------------
# match_found = False

# for po in po_list:

#     po_vendor = str(
#         po.get("vendor") or
#         po.get("vendor_name") or
#         po.get("supplier") or
#         ""
#     ).lower()

#     po_amount = safe_float(po.get("total_amount"))

#     if po_vendor in vendor or vendor in po_vendor:

#         match_found = True

#         if abs(po_amount - invoice_amount) < 5:
#             status = "APPROVED"
#         else:
#             reasons.append("Amount mismatch with PO")

#         break


# if not match_found:
#     reasons.append("No matching Purchase Order found")


# # -----------------------------
# # SAVE RESULT
# # -----------------------------
# result = {
#     "status": status,
#     "reasons": reasons
# }

# OUTPUT_FILE.write_text(json.dumps(result, indent=4))

# print("✅ 3-WAY MATCHING COMPLETED")



from pathlib import Path
import json
import sys

# -------------------------------------------------
# 🔥 FIX: ADD PROJECT ROOT TO PYTHON PATH
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR))

# ✅ NOW THIS IMPORT WILL WORK
from backend.database.mongo import invoices_collection

# -------------------------------------------------
# PATHS
# -------------------------------------------------
INVOICE_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"
PO_FILE = BASE_DIR / "data" / "purchase_orders.json"

OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"


# -----------------------------
# SAFE FLOAT FUNCTION
# -----------------------------
def safe_float(value, default=0.0):
    if value in [None, "null", "None", ""]:
        return default

    try:
        return float(value)
    except:
        return default


# -----------------------------
# LOAD FILES
# -----------------------------
invoice = json.loads(INVOICE_FILE.read_text())
po_list = json.loads(PO_FILE.read_text())


# -----------------------------
# EXTRACT INVOICE DATA
# -----------------------------
vendor = str(invoice.get("vendor_name", "")).lower()
invoice_amount = safe_float(invoice.get("total_amount"))
invoice_number = str(invoice.get("invoice_number", "")).lower()


# -----------------------------
# INITIAL STATUS
# -----------------------------
status = "FLAGGED"
reasons = []


# -----------------------------
# DUPLICATE CHECK (MONGODB)
# -----------------------------
existing_invoice = invoices_collection.find_one({
    "invoice_number": invoice.get("invoice_number"),
    "vendor_name": invoice.get("vendor_name")
})

if existing_invoice:
    result = {
        "status": "REJECTED",
        "reasons": ["Duplicate invoice detected (DB)"]
    }

    OUTPUT_FILE.write_text(json.dumps(result, indent=4))
    print("❌ DUPLICATE INVOICE FOUND (DB)")

    sys.exit()   # Stop execution completely


# -----------------------------
# MATCH PO (3-WAY MATCHING)
# -----------------------------
match_found = False

for po in po_list:

    po_vendor = str(
        po.get("vendor") or
        po.get("vendor_name") or
        po.get("supplier") or
        ""
    ).lower()

    po_amount = safe_float(po.get("total_amount"))

    if po_vendor in vendor or vendor in po_vendor:

        match_found = True

        if abs(po_amount - invoice_amount) < 5:
            status = "APPROVED"
        else:
            reasons.append("Amount mismatch with PO")

        break


if not match_found:
    reasons.append("No matching Purchase Order found")


# -----------------------------
# SAVE RESULT
# -----------------------------
result = {
    "status": status,
    "reasons": reasons
}

OUTPUT_FILE.write_text(json.dumps(result, indent=4))

print("✅ 3-WAY MATCHING COMPLETED")