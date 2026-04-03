

# from fastapi import FastAPI, UploadFile, File
# from pathlib import Path
# import shutil
# import subprocess
# import sys
# import json
# import time   # ✅ ADDED

# from backend.database.mongo import invoices_collection

# app = FastAPI(title="Invoice Automation API")

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# UPLOAD_DIR = BASE_DIR / "invoices" / "raw"
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# PIPELINE_SCRIPT = BASE_DIR / "run_pipeline.py"

# AI_RESULT_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"

# VERIFICATION_FILE = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"

# # -------------------------------------------------
# # SAFE FLOAT
# # -------------------------------------------------

# def safe_float(value, default=0.0):
#     if value in [None, "null", "None", ""]:
#         return default
#     try:
#         return float(value)
#     except:
#         return default

# # -------------------------------------------------
# # HOME
# # -------------------------------------------------

# @app.get("/")
# def home():
#     return {"message": "Invoice Automation API Running"}

# # -------------------------------------------------
# # PROCESS INVOICE
# # -------------------------------------------------

# @app.post("/process-invoice")
# async def process_invoice(file: UploadFile = File(...)):

#     try:

#         start_time = time.time()   # ✅ START TIMER

#         file_path = UPLOAD_DIR / file.filename

#         # Save uploaded invoice
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Run pipeline
#         subprocess.run(
#             [sys.executable, str(PIPELINE_SCRIPT)],
#             cwd=BASE_DIR,
#             check=True
#         )

#         # -----------------------------
#         # LOAD AI EXTRACTION RESULT
#         # -----------------------------

#         if not AI_RESULT_FILE.exists():
#             return {"error": "Extraction failed"}

#         invoice_data = json.loads(AI_RESULT_FILE.read_text())

#         total_amount = safe_float(invoice_data.get("total_amount"))

#         # -----------------------------
#         # LOAD VERIFICATION RESULT
#         # -----------------------------

#         status = None
#         reasons = []

#         if VERIFICATION_FILE.exists():
#             verification = json.loads(VERIFICATION_FILE.read_text())
#             status = verification.get("status")
#             reasons = verification.get("reasons", [])

#         # -----------------------------
#         # DATABASE RECORD
#         # -----------------------------

#         invoice_record = {
#             "vendor_name": invoice_data.get("vendor_name"),
#             "gstin": invoice_data.get("gstin"),
#             "invoice_number": invoice_data.get("invoice_number"),
#             "invoice_date": invoice_data.get("invoice_date"),
#             "total_amount": total_amount,
#             "status": status
#         }

#         result = invoices_collection.insert_one(invoice_record)

#         end_time = time.time()   # ✅ END TIMER
#         processing_time = round(end_time - start_time, 2)

#         return {
#             "invoice_id": str(result.inserted_id),
#             "vendor_name": invoice_record["vendor_name"],
#             "gstin": invoice_record["gstin"],
#             "invoice_number": invoice_record["invoice_number"],
#             "invoice_date": invoice_record["invoice_date"],
#             "total_amount": invoice_record["total_amount"],
#             "status": status,
#             "reasons": reasons,
#             "processing_time": processing_time   # ✅ NEW FIELD
#         }

#     except Exception as e:
#         return {"error": str(e)}

# # -------------------------------------------------
# # GET ALL INVOICES
# # -------------------------------------------------

# @app.get("/invoices")
# def get_all_invoices():

#     try:

#         invoices = []

#         for inv in invoices_collection.find():

#             invoices.append({
#                 "id": str(inv["_id"]),
#                 "vendor_name": inv.get("vendor_name"),
#                 "gstin": inv.get("gstin"),
#                 "invoice_number": inv.get("invoice_number"),
#                 "invoice_date": inv.get("invoice_date"),
#                 "total_amount": inv.get("total_amount"),
#                 "status": inv.get("status")
#             })

#         return invoices

#     except Exception as e:
#         return {"error": str(e)}







from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil
import subprocess
import sys
import json
import time

from backend.database.mongo import invoices_collection

app = FastAPI(title="Invoice Automation API")

# -------------------------------------------------
# PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "invoices" / "raw"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PIPELINE_SCRIPT = BASE_DIR / "run_pipeline.py"

AI_RESULT_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"
VERIFICATION_FILE = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"

# -------------------------------------------------
# GLOBAL CONTROL (NEW - prevents duplicate execution)
# -------------------------------------------------

is_processing = False
last_processed_file = None
last_processed_time = 0

# -------------------------------------------------
# SAFE FLOAT
# -------------------------------------------------

def safe_float(value, default=0.0):
    if value in [None, "null", "None", ""]:
        return default
    try:
        return float(value)
    except:
        return default

# -------------------------------------------------
# HOME
# -------------------------------------------------

@app.get("/")
def home():
    return {"message": "Invoice Automation API Running"}

# -------------------------------------------------
# PROCESS INVOICE
# -------------------------------------------------

@app.post("/process-invoice")
async def process_invoice(file: UploadFile = File(...)):

    global is_processing, last_processed_file, last_processed_time

    try:
        # ---------------------------------
        # PREVENT MULTIPLE TRIGGERS
        # ---------------------------------

        current_time = time.time()

        if is_processing:
            return {"message": "⚠️ Already processing an invoice. Please wait."}

        # Prevent same file triggering again within 5 seconds
        if (
            last_processed_file == file.filename and
            (current_time - last_processed_time) < 5
        ):
            return {"message": "⚠️ Duplicate request ignored"}

        is_processing = True
        last_processed_file = file.filename
        last_processed_time = current_time

        start_time = time.time()

        file_path = UPLOAD_DIR / file.filename

        # Save uploaded invoice
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run pipeline
        subprocess.run(
            [sys.executable, str(PIPELINE_SCRIPT)],
            cwd=BASE_DIR,
            check=True
        )

        # -----------------------------
        # LOAD AI EXTRACTION RESULT
        # -----------------------------

        if not AI_RESULT_FILE.exists():
            return {"error": "Extraction failed"}

        invoice_data = json.loads(AI_RESULT_FILE.read_text())

        total_amount = safe_float(invoice_data.get("total_amount"))

        # -----------------------------
        # LOAD VERIFICATION RESULT
        # -----------------------------

        status = None
        reasons = []

        if VERIFICATION_FILE.exists():
            verification = json.loads(VERIFICATION_FILE.read_text())
            status = verification.get("status")
            reasons = verification.get("reasons", [])

        # -----------------------------
        # DATABASE RECORD
        # -----------------------------

        invoice_record = {
            "vendor_name": invoice_data.get("vendor_name"),
            "gstin": invoice_data.get("gstin"),
            "invoice_number": invoice_data.get("invoice_number"),
            "invoice_date": invoice_data.get("invoice_date"),
            "total_amount": total_amount,
            "status": status
        }

        result = invoices_collection.insert_one(invoice_record)

        end_time = time.time()
        processing_time = round(end_time - start_time, 2)

        return {
            "invoice_id": str(result.inserted_id),
            "vendor_name": invoice_record["vendor_name"],
            "gstin": invoice_record["gstin"],
            "invoice_number": invoice_record["invoice_number"],
            "invoice_date": invoice_record["invoice_date"],
            "total_amount": invoice_record["total_amount"],
            "status": status,
            "reasons": reasons,
            "processing_time": processing_time
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        # ALWAYS release lock
        is_processing = False


# -------------------------------------------------
# GET ALL INVOICES
# -------------------------------------------------

@app.get("/invoices")
def get_all_invoices():

    try:

        invoices = []

        for inv in invoices_collection.find():

            invoices.append({
                "id": str(inv["_id"]),
                "vendor_name": inv.get("vendor_name"),
                "gstin": inv.get("gstin"),
                "invoice_number": inv.get("invoice_number"),
                "invoice_date": inv.get("invoice_date"),
                "total_amount": inv.get("total_amount"),
                "status": inv.get("status")
            })

        return invoices

    except Exception as e:
        return {"error": str(e)}