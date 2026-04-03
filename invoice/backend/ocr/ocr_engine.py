# import pytesseract
# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# from pathlib import Path
# from paddleocr import PaddleOCR

# # ---------------------------------------
# # Windows Tesseract Path
# # ---------------------------------------

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # ---------------------------------------
# # Load PaddleOCR model once
# # ---------------------------------------

# print("Loading OCR Model...")

# paddle_ocr = PaddleOCR(
#     lang="en",
#     use_textline_orientation=True
# )

# print("OCR Model Ready")


# # ---------------------------------------
# # Project Paths
# # ---------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# INVOICE_DIR = BASE_DIR / "invoices" / "raw"
# OUTPUT_DIR = BASE_DIR / "output" / "extracted_text"

# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# # ---------------------------------------
# # IMAGE PREPROCESSING
# # ---------------------------------------

# def preprocess_image(img):

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     gray = cv2.GaussianBlur(gray, (5,5), 0)

#     thresh = cv2.adaptiveThreshold(
#         gray,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     return thresh


# # ---------------------------------------
# # Paddle OCR
# # ---------------------------------------

# def paddle_extract(image):

#     result = paddle_ocr.ocr(image)

#     text_lines = []

#     if result:

#         for line in result[0]:

#             text_lines.append(line[1][0])

#     return "\n".join(text_lines)


# # ---------------------------------------
# # Tesseract OCR fallback
# # ---------------------------------------

# def tesseract_extract(img):

#     return pytesseract.image_to_string(img)


# # ---------------------------------------
# # IMAGE OCR
# # ---------------------------------------

# def extract_text_from_image(image_path):

#     img = cv2.imread(str(image_path))

#     if img is None:
#         raise Exception("Image could not be read")

#     processed = preprocess_image(img)

#     # Try PaddleOCR first
#     try:

#         text = paddle_extract(img)

#         if len(text) > 50:
#             return text

#     except Exception as e:

#         print("PaddleOCR failed:", e)

#     print("Using Tesseract fallback")

#     return tesseract_extract(processed)


# # ---------------------------------------
# # PDF OCR
# # ---------------------------------------

# def extract_text_from_pdf(pdf_path):

#     pages = convert_from_path(pdf_path, dpi=300)

#     full_text = ""

#     for page in pages:

#         # Convert PIL image to OpenCV format
#         img = cv2.cvtColor(
#             np.array(page),
#             cv2.COLOR_RGB2BGR
#         )

#         processed = preprocess_image(img)

#         try:

#             text = paddle_extract(img)

#             if len(text) < 50:
#                 text = tesseract_extract(processed)

#         except:

#             text = tesseract_extract(processed)

#         full_text += text + "\n"

#     return full_text


# # ---------------------------------------
# # MAIN OCR ROUTER
# # ---------------------------------------

# def extract_invoice_text(file_path):

#     file_path = Path(file_path)

#     if file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:

#         return extract_text_from_image(file_path)

#     elif file_path.suffix.lower() == ".pdf":

#         return extract_text_from_pdf(file_path)

#     else:

#         raise ValueError("Unsupported file type")


# # ---------------------------------------
# # CLI RUN (for testing)
# # ---------------------------------------

# if __name__ == "__main__":

#     invoice_files = sorted(
#         INVOICE_DIR.glob("*"),
#         key=lambda x: x.stat().st_mtime,
#         reverse=True
#     )

#     if not invoice_files:

#         raise FileNotFoundError("No invoice found in invoices/raw")

#     invoice_path = invoice_files[0]

#     print("\nProcessing invoice:", invoice_path.name)

#     text = extract_invoice_text(invoice_path)

#     output_file = OUTPUT_DIR / "invoice_text.txt"

#     output_file.write_text(text, encoding="utf-8")

#     print("\nOCR completed")

#     print("Saved to:", output_file)



# from paddleocr import PaddleOCR
# from pdf2image import convert_from_path
# import pytesseract
# import cv2
# import numpy as np
# from pathlib import Path
# import shutil

# # -------------------------------------------------
# # Tesseract path (Windows)
# # -------------------------------------------------

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # -------------------------------------------------
# # LOAD OCR MODEL
# # -------------------------------------------------

# print("Loading OCR Model...")

# ocr = PaddleOCR(
#     lang="en",
#     use_angle_cls=False
# )

# print("OCR Model Ready")

# # -------------------------------------------------
# # PROJECT PATHS
# # -------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# INPUT_DIR = BASE_DIR / "invoices" / "raw"
# OUTPUT_DIR = BASE_DIR / "output" / "extracted_text"

# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# # -------------------------------------------------
# # CLEAR OLD OCR OUTPUT
# # -------------------------------------------------

# def clear_old_outputs():

#     if OUTPUT_DIR.exists():
#         shutil.rmtree(OUTPUT_DIR)

#     OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# # -------------------------------------------------
# # GET LATEST INVOICE
# # -------------------------------------------------

# def get_latest_invoice():

#     files = sorted(
#         [f for f in INPUT_DIR.glob("*") if f.suffix.lower() in [".pdf",".png",".jpg",".jpeg"]],
#         key=lambda x: x.stat().st_mtime
#     )

#     if not files:
#         raise Exception("❌ No invoice found inside invoices/raw")

#     return files[-1]

# # -------------------------------------------------
# # IMAGE PREPROCESS
# # -------------------------------------------------

# def preprocess(img):

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     blur = cv2.GaussianBlur(gray, (5,5), 0)

#     thresh = cv2.adaptiveThreshold(
#         blur,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     return thresh

# # -------------------------------------------------
# # PADDLE OCR
# # -------------------------------------------------

# def paddle_extract(img):

#     result = ocr.ocr(img)

#     lines = []

#     if result:

#         for line in result[0]:

#             text = line[1][0]
#             conf = line[1][1]

#             if conf > 0.6:
#                 lines.append(text)

#     return lines

# # -------------------------------------------------
# # TESSERACT FALLBACK
# # -------------------------------------------------

# def tesseract_extract(img):

#     text = pytesseract.image_to_string(img)

#     return text.split("\n")

# # -------------------------------------------------
# # IMAGE OCR
# # -------------------------------------------------

# def extract_from_image(path):

#     img = cv2.imread(str(path))

#     if img is None:
#         raise Exception("❌ Could not read image")

#     processed = preprocess(img)

#     try:

#         lines = paddle_extract(img)

#         if len(lines) > 10:
#             return lines

#     except Exception as e:

#         print("PaddleOCR failed:", e)

#     print("Using Tesseract fallback")

#     return tesseract_extract(processed)

# # -------------------------------------------------
# # PDF OCR
# # -------------------------------------------------

# def extract_from_pdf(pdf):

#     pages = convert_from_path(pdf, dpi=120)

#     all_lines = []

#     for page in pages:

#         img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

#         processed = preprocess(img)

#         try:

#             lines = paddle_extract(img)

#             if len(lines) < 10:
#                 lines = tesseract_extract(processed)

#         except:

#             lines = tesseract_extract(processed)

#         all_lines.extend(lines)

#     return all_lines

# # -------------------------------------------------
# # MAIN OCR RUNNER
# # -------------------------------------------------

# def run_ocr():

#     clear_old_outputs()

#     invoice = get_latest_invoice()

#     print("\nProcessing invoice:", invoice.name)

#     if invoice.suffix.lower() == ".pdf":

#         lines = extract_from_pdf(invoice)

#     else:

#         lines = extract_from_image(invoice)

#     text = "\n".join(lines)

#     output_file = OUTPUT_DIR / "invoice_text.txt"

#     output_file.write_text(text, encoding="utf-8")

#     print("\n✅ OCR completed")
#     print("Saved to:", output_file)

# # -------------------------------------------------
# # RUN
# # -------------------------------------------------

# if __name__ == "__main__":

#     run_ocr()






# from paddleocr import PaddleOCR
# from pdf2image import convert_from_path
# import pytesseract
# import cv2
# import numpy as np
# from pathlib import Path
# import shutil

# # -------------------------------------------------
# # Tesseract path (Windows)
# # -------------------------------------------------

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # -------------------------------------------------
# # LOAD OCR MODEL
# # -------------------------------------------------

# print("Loading OCR Model...")

# ocr = PaddleOCR(
#     lang="en",
#     use_textline_orientation=False
# )

# print("OCR Model Ready")

# # -------------------------------------------------
# # PROJECT PATHS
# # -------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# INPUT_DIR = BASE_DIR / "invoices" / "raw"
# OUTPUT_DIR = BASE_DIR / "output" / "extracted_text"

# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# # -------------------------------------------------
# # CLEAR OLD OUTPUT
# # -------------------------------------------------

# def clear_old_outputs():

#     if OUTPUT_DIR.exists():
#         shutil.rmtree(OUTPUT_DIR)

#     OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# # -------------------------------------------------
# # GET LATEST INVOICE
# # -------------------------------------------------

# def get_latest_invoice():

#     files = sorted(
#         [f for f in INPUT_DIR.glob("*") if f.suffix.lower() in [".pdf",".png",".jpg",".jpeg"]],
#         key=lambda x: x.stat().st_mtime
#     )

#     if not files:
#         raise Exception("❌ No invoice found inside invoices/raw")

#     return files[-1]


# # -------------------------------------------------
# # IMAGE PREPROCESS
# # -------------------------------------------------

# def preprocess(img):

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     blur = cv2.GaussianBlur(gray, (5,5), 0)

#     thresh = cv2.adaptiveThreshold(
#         blur,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     return thresh


# # -------------------------------------------------
# # PADDLE OCR
# # -------------------------------------------------

# def paddle_extract(img):

#     result = ocr.predict(img)

#     lines = []

#     if result:

#         for block in result:

#             for line in block:

#                 text = line[1][0]
#                 conf = line[1][1]

#                 if conf > 0.6:
#                     lines.append(text)

#     return lines


# # -------------------------------------------------
# # TESSERACT FALLBACK
# # -------------------------------------------------

# def tesseract_extract(img):

#     text = pytesseract.image_to_string(img)

#     return text.split("\n")


# # -------------------------------------------------
# # IMAGE OCR
# # -------------------------------------------------

# def extract_from_image(path):

#     img = cv2.imread(str(path))

#     if img is None:
#         raise Exception("❌ Could not read image")

#     processed = preprocess(img)

#     try:

#         lines = paddle_extract(img)

#         if len(lines) > 10:
#             return lines

#     except Exception as e:

#         print("PaddleOCR failed:", e)

#     print("Using Tesseract fallback")

#     return tesseract_extract(processed)


# # -------------------------------------------------
# # PDF OCR
# # -------------------------------------------------

# def extract_from_pdf(pdf):

#     pages = convert_from_path(pdf, dpi=90)

#     all_lines = []

#     for page in pages:

#         img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

#         processed = preprocess(img)

#         try:

#             lines = paddle_extract(img)

#             if len(lines) < 10:
#                 lines = tesseract_extract(processed)

#         except:
#             lines = tesseract_extract(processed)

#         all_lines.extend(lines)

#     return all_lines


# # -------------------------------------------------
# # RUN OCR
# # -------------------------------------------------

# def run_ocr():

#     clear_old_outputs()

#     invoice = get_latest_invoice()

#     print("\nProcessing invoice:", invoice.name)

#     if invoice.suffix.lower() == ".pdf":

#         lines = extract_from_pdf(invoice)

#     else:

#         lines = extract_from_image(invoice)

#     text = "\n".join(lines)

#     output_file = OUTPUT_DIR / "invoice_text.txt"

#     output_file.write_text(text, encoding="utf-8")

#     print("\n✅ OCR completed")
#     print("Saved to:", output_file)


# # -------------------------------------------------
# # MAIN
# # -------------------------------------------------

# if __name__ == "__main__":

#     run_ocr()















import os
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

from paddleocr import PaddleOCR
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from pathlib import Path
import shutil
import logging

logging.getLogger().setLevel(logging.ERROR)

# -------------------------------------------------
# Tesseract path (Windows)
# -------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------------------------------------
# LOAD OCR MODEL
# -------------------------------------------------

print("Loading OCR Model...")

ocr = PaddleOCR(
    lang="en",
    use_angle_cls=False
)

print("OCR Model Ready")

# -------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "invoices" / "raw"
OUTPUT_DIR = BASE_DIR / "output" / "extracted_text"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# CLEAR OLD OUTPUT
# -------------------------------------------------

def clear_old_outputs():

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# GET LATEST INVOICE
# -------------------------------------------------

def get_latest_invoice():

    files = sorted(
        [f for f in INPUT_DIR.glob("*") if f.suffix.lower() in [".pdf",".png",".jpg",".jpeg"]],
        key=lambda x: x.stat().st_mtime
    )

    if not files:
        raise Exception("❌ No invoice found inside invoices/raw")

    return files[-1]


# -------------------------------------------------
# IMAGE PREPROCESS
# -------------------------------------------------

def preprocess(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


# -------------------------------------------------
# PADDLE OCR
# -------------------------------------------------

def paddle_extract(img):

    result = ocr.predict(img)

    lines = []

    if result:

        for block in result:

            if not block:
                continue

            for line in block:

                text = line[1][0]
                conf = line[1][1]

                if conf > 0.6:
                    lines.append(text)

    return lines


# -------------------------------------------------
# TESSERACT FALLBACK
# -------------------------------------------------

def tesseract_extract(img):

    text = pytesseract.image_to_string(img)

    return text.split("\n")


# -------------------------------------------------
# IMAGE OCR
# -------------------------------------------------

def extract_from_image(path):

    img = cv2.imread(str(path))

    if img is None:
        raise Exception("❌ Could not read image")

    processed = preprocess(img)

    try:

        lines = paddle_extract(img)

        if len(lines) > 10:
            return lines

    except Exception as e:

        print("PaddleOCR failed:", e)

    print("Using Tesseract fallback")

    return tesseract_extract(processed)


# -------------------------------------------------
# PDF OCR
# -------------------------------------------------

def extract_from_pdf(pdf):

    pages = convert_from_path(pdf, dpi=60)

    all_lines = []

    for page in pages:

        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        processed = preprocess(img)

        try:

            lines = paddle_extract(img)

            if len(lines) < 10:
                lines = tesseract_extract(processed)

        except:
            lines = tesseract_extract(processed)

        all_lines.extend(lines)

    return all_lines


# -------------------------------------------------
# RUN OCR
# -------------------------------------------------

def run_ocr():

    clear_old_outputs()

    invoice = get_latest_invoice()

    print("\nProcessing invoice:", invoice.name)

    if invoice.suffix.lower() == ".pdf":

        lines = extract_from_pdf(invoice)

    else:

        lines = extract_from_image(invoice)

    text = "\n".join(lines)

    output_file = OUTPUT_DIR / "invoice_text.txt"

    output_file.write_text(text, encoding="utf-8")

    print("\n✅ OCR completed")
    print("Saved to:", output_file)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    run_ocr()