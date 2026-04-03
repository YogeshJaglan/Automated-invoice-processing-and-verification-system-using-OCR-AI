# from pathlib import Path
# import subprocess
# import sys

# BASE_DIR = Path(__file__).resolve().parent

# SCRIPTS = [

#     BASE_DIR / "backend" / "ocr" / "ocr_engine.py",

#     BASE_DIR / "backend" / "extraction" / "invoice_ai_extractor.py",

# ]

# def run_script(script_path):

#     print("\n----------------------------------")
#     print(f"🚀 Running: {script_path.name}")
#     print("----------------------------------")

#     result = subprocess.run(
#         [sys.executable, str(script_path)],
#         cwd=script_path.parent
#     )

#     if result.returncode != 0:
#         print(f"\n❌ ERROR while running {script_path.name}")
#         sys.exit(1)

#     print(f"✅ Completed: {script_path.name}")


# if __name__ == "__main__":

#     print("\n===================================")
#     print("🧾 INVOICE PIPELINE START")
#     print("===================================")

#     for script in SCRIPTS:

#         if not script.exists():
#             print("\n❌ Script not found:")
#             print(script)
#             sys.exit(1)

#         run_script(script)

#     print("\n===================================")
#     print("✅ INVOICE PIPELINE COMPLETED")
#     print("===================================")








from pathlib import Path
import subprocess
import sys

# -------------------------------------------------
# PROJECT ROOT
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# -------------------------------------------------
# PIPELINE STEPS
# -------------------------------------------------

SCRIPTS = [

    # 1️⃣ OCR Extraction
    BASE_DIR / "backend" / "ocr" / "ocr_engine.py",

    # 2️⃣ AI Invoice Field Extraction (Ollama / LLM)
    BASE_DIR / "backend" / "extraction" / "invoice_ai_extractor.py",

    # 3️⃣ GST Validation
    BASE_DIR / "backend" / "verification" / "gst_calculator.py",

    # 4️⃣ Three Way Match (PO + Delivery + Invoice)
    BASE_DIR / "backend" / "verification" / "three_way_match.py",
]

# -------------------------------------------------
# FINAL OUTPUT FILE
# -------------------------------------------------

FINAL_RESULT = BASE_DIR / "output" / "structured_data" / "final_verification_result.json"


# -------------------------------------------------
# SCRIPT RUNNER
# -------------------------------------------------

def run_script(script):

    print("\n----------------------------------")
    print(f"🚀 Running: {script.name}")
    print("----------------------------------")

    try:

        subprocess.run(
            [sys.executable, str(script)],
            cwd=script.parent,
            check=True
        )

        print(f"✅ Completed: {script.name}")

    except subprocess.CalledProcessError as e:

        print(f"\n❌ ERROR while running {script.name}")
        print(e)

        sys.exit(1)


# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("🧾 INVOICE AUTOMATION PIPELINE START")
    print("===================================")

    # Check scripts exist
    for script in SCRIPTS:

        if not script.exists():

            print("\n❌ Script not found:")
            print(script)

            sys.exit(1)

    # Run scripts sequentially
    for script in SCRIPTS:
        run_script(script)

    print("\n===================================")
    print("✅ INVOICE PIPELINE COMPLETED")
    print("===================================")

    # Show final result if exists
    if FINAL_RESULT.exists():

        print("\n📊 FINAL VERIFICATION RESULT:\n")
        print(FINAL_RESULT.read_text())

    else:

        print("\n⚠ Final verification file not found.")