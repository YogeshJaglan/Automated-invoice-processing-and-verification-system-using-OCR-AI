# from fastapi import FastAPI, UploadFile, File
# from pathlib import Path
# import shutil
# import subprocess
# import sys
# import json
# import re

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

#         file_path = UPLOAD_DIR / file.filename

#         # Save invoice
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Run pipeline
#         subprocess.run(
#             [sys.executable, str(PIPELINE_SCRIPT)],
#             cwd=BASE_DIR,
#             check=True
#         )

#         # Check if extraction file exists
#         if not AI_RESULT_FILE.exists():
#             return {"error": "Extraction failed"}

#         invoice_data = json.loads(AI_RESULT_FILE.read_text())

#         # -----------------------------------------
#         # SAFE AMOUNT PARSING
#         # -----------------------------------------

#         amount_text = str(invoice_data.get("total_amount", "0"))

#         numbers = re.findall(r"\d+\.?\d*", amount_text)

#         if numbers:
#             total_amount = float(numbers[0])
#         else:
#             total_amount = 0.0

#         # -----------------------------------------
#         # CREATE RECORD
#         # -----------------------------------------

#         invoice_record = {
#             "vendor_name": invoice_data.get("vendor_name"),
#             "gstin": invoice_data.get("gstin"),
#             "invoice_number": invoice_data.get("invoice_number"),
#             "invoice_date": invoice_data.get("invoice_date"),
#             "total_amount": total_amount
#         }

#         result = invoices_collection.insert_one(invoice_record)

#         return {
#             "invoice_id": str(result.inserted_id),
#             "vendor_name": invoice_record["vendor_name"],
#             "gstin": invoice_record["gstin"],
#             "invoice_number": invoice_record["invoice_number"],
#             "invoice_date": invoice_record["invoice_date"],
#             "total_amount": invoice_record["total_amount"]
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
#                 "total_amount": inv.get("total_amount")
#             })

#         return invoices

#     except Exception as e:

#         return {"error": str(e)}




# from fastapi import FastAPI, UploadFile, File
# from pathlib import Path
# import shutil
# import subprocess
# import sys
# import json
# import re

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

#         # -----------------------------
#         # SAFE AMOUNT PARSING
#         # -----------------------------

#         amount_text = str(invoice_data.get("total_amount", "0"))

#         numbers = re.findall(r"\d+\.?\d*", amount_text)

#         if numbers:
#             total_amount = float(numbers[0])
#         else:
#             total_amount = 0.0

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
#         # CREATE DATABASE RECORD
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

#         return {
#             "invoice_id": str(result.inserted_id),
#             "vendor_name": invoice_record["vendor_name"],
#             "gstin": invoice_record["gstin"],
#             "invoice_number": invoice_record["invoice_number"],
#             "invoice_date": invoice_record["invoice_date"],
#             "total_amount": invoice_record["total_amount"],
#             "status": status,
#             "reasons": reasons
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

    try:

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

        # -----------------------------
        # SAFE AMOUNT FROM AI
        # -----------------------------

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

        return {
            "invoice_id": str(result.inserted_id),
            "vendor_name": invoice_record["vendor_name"],
            "gstin": invoice_record["gstin"],
            "invoice_number": invoice_record["invoice_number"],
            "invoice_date": invoice_record["invoice_date"],
            "total_amount": invoice_record["total_amount"],
            "status": status,
            "reasons": reasons
        }

    except Exception as e:

        return {"error": str(e)}

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