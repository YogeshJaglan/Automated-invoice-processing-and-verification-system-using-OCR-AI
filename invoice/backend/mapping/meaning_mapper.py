from pathlib import Path
import re

# -------------------------------------------------
# PROJECT ROOT (invoice/)
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "output" / "cleaned_text" / "cleaned_invoice_text.txt"
OUTPUT_DIR = BASE_DIR / "output" / "structured_data"
OUTPUT_FILE = OUTPUT_DIR / "semantic_output.txt"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# SEMANTIC EXTRACTION LOGIC
# -------------------------------------------------

def extract_semantic_data(lines):
    results = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # ---------- VENDOR NAME (MULTI-LINE) ----------
        if "sold by" in line and "VENDOR_NAME" not in results:
            vendor_parts = []
            j = i + 1
            while j < len(lines) and len(lines[j].strip()) > 3:
                vendor_parts.append(lines[j].strip())
                if "pvt ltd" in lines[j] or "private limited" in lines[j]:
                    break
                j += 1
            if vendor_parts:
                results["VENDOR_NAME"] = " ".join(vendor_parts)

        # ---------- GSTIN (STRICT + FALLBACK) ----------
        if "gst" in line and "GSTIN" not in results and "GSTIN_UNVERIFIED" not in results:
            strict = re.search(
                r"\b[0-9]{2}[a-z]{5}[0-9]{4}[a-z][a-z0-9]z[a-z0-9]\b",
                line
            )
            if strict:
                results["GSTIN"] = strict.group().upper()
            else:
                loose = re.search(r"\b[0-9a-z]{13,15}\b", line)
                if loose:
                    results["GSTIN_UNVERIFIED"] = loose.group().upper()

        # ---------- DATE ----------
        if "date" in line and "DATE" not in results:
            match = re.search(r"\d{2}[./-]\d{2}[./-]\d{4}", line)
            if match:
                results["DATE"] = match.group()

        # ---------- INVOICE NUMBER ----------
        if "invoice number" in line and "INVOICE_NUMBER" not in results:
            value = line.replace("invoice number", "").strip()
            if value:
                results["INVOICE_NUMBER"] = value

        # ---------- TOTAL AMOUNT ----------
        if "TOTAL_AMOUNT" not in results:
            amount_match = re.fullmatch(r"\d+(\.\d{2})", line)
            if amount_match:
                results["TOTAL_AMOUNT"] = amount_match.group()

        i += 1

    return results

# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    print("🔍 Looking for cleaned file at:")
    print(INPUT_FILE.resolve())

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"❌ Cleaned invoice text file not found at:\n{INPUT_FILE.resolve()}"
        )

    lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()

    semantic_data = extract_semantic_data(lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for key, value in semantic_data.items():
            f.write(f"{key} : {value}\n")

    print("✅ SEMANTIC MEANING EXTRACTION COMPLETED")
    print("📄 Output saved at:", OUTPUT_FILE.resolve())
