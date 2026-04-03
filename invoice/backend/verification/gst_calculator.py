import json
from pathlib import Path

# -------------------------------------------------
# PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INVOICE_FILE = BASE_DIR / "output" / "structured_data" / "final_invoice.json"
OUTPUT_FILE = BASE_DIR / "output" / "structured_data" / "gst_verification.json"


# -------------------------------------------------
# LOAD INVOICE DATA
# -------------------------------------------------

invoice = json.loads(INVOICE_FILE.read_text())


# -------------------------------------------------
# SAFE NUMBER CONVERTER
# -------------------------------------------------

def safe_float(value, default=0.0):

    if value in [None, "null", "None", ""]:
        return default

    try:
        return float(value)
    except:
        return default


# -------------------------------------------------
# EXTRACT VALUES
# -------------------------------------------------

total_amount = safe_float(invoice.get("total_amount"))

gst_rate = 18   # default GST


# -------------------------------------------------
# CALCULATE EXPECTED GST
# -------------------------------------------------

expected_gst = round(total_amount * gst_rate / 100, 2)


# -------------------------------------------------
# INVOICE GST
# -------------------------------------------------

invoice_gst = safe_float(invoice.get("gst_amount"), expected_gst)


# -------------------------------------------------
# VERIFY GST
# -------------------------------------------------

if abs(invoice_gst - expected_gst) < 2:

    gst_status = "VALID"

else:

    gst_status = "MISMATCH"


# -------------------------------------------------
# SAVE RESULT
# -------------------------------------------------

result = {
    "total_amount": total_amount,
    "expected_gst": expected_gst,
    "invoice_gst": invoice_gst,
    "gst_status": gst_status
}

OUTPUT_FILE.write_text(json.dumps(result, indent=4))


print("GST verification completed")