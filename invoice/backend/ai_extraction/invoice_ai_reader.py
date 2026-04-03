# from paddleocr import PPStructureV3
# from pdf2image import convert_from_path
# import cv2
# from pathlib import Path
# import json
# import traceback

# # ---------------------------------------------------
# # PROJECT PATHS
# # ---------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parents[2]

# INPUT_DIR = BASE_DIR / "invoices" / "raw"
# OUTPUT_DIR = BASE_DIR / "output" / "ai_extraction"

# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# # ---------------------------------------------------
# # LOAD MODEL
# # ---------------------------------------------------

# print("\nLoading PaddleOCR Structure Model...")

# try:
#     engine = PPStructureV3()
#     print("Model Loaded Successfully\n")

# except Exception as e:
#     print("Model loading failed")
#     print(e)
#     exit()

# # ---------------------------------------------------
# # GET LATEST INVOICE
# # ---------------------------------------------------

# def get_latest_invoice():

#     files = list(INPUT_DIR.glob("*"))

#     if not files:
#         raise Exception("No invoice found inside invoices/raw")

#     latest = max(files, key=lambda x: x.stat().st_mtime)

#     return latest


# # ---------------------------------------------------
# # PDF → IMAGE
# # ---------------------------------------------------

# def convert_pdf_to_images(pdf_path):

#     pages = convert_from_path(pdf_path, dpi=300)

#     image_paths = []

#     for i, page in enumerate(pages):

#         img_path = OUTPUT_DIR / f"page_{i}.jpg"

#         page.save(img_path, "JPEG")

#         image_paths.append(str(img_path))

#     return image_paths


# # ---------------------------------------------------
# # IMAGE PROCESSING
# # ---------------------------------------------------

# def process_image(img_path):

#     try:

#         img = cv2.imread(img_path)

#         if img is None:
#             print("Failed to read image:", img_path)
#             return []

#         results = engine.predict(img)

#         return results

#     except Exception as e:

#         print("Image processing error:", e)

#         return []


# # ---------------------------------------------------
# # TEXT EXTRACTION
# # ---------------------------------------------------

# def extract_text_blocks(results):

#     text_blocks = []

#     for block in results:

#         try:

#             block_type = block.get("type")

#             if block_type == "text":

#                 lines = block.get("res", [])

#                 for line in lines:

#                     if isinstance(line, dict):

#                         txt = line.get("text")

#                         if txt:
#                             text_blocks.append(txt)

#             elif block_type == "table":

#                 table = block.get("res", {})

#                 html = table.get("html")

#                 if html:
#                     text_blocks.append(html)

#         except Exception as e:

#             continue

#     return text_blocks


# # ---------------------------------------------------
# # CLEAN TEXT
# # ---------------------------------------------------

# def clean_text_blocks(blocks):

#     cleaned = []

#     for b in blocks:

#         try:

#             text = str(b).strip()

#             if len(text) < 2:
#                 continue

#             cleaned.append(text)

#         except:
#             continue

#     return cleaned


# # ---------------------------------------------------
# # SAVE RESULT
# # ---------------------------------------------------

# def save_ai_output(text_blocks):

#     output_file = OUTPUT_DIR / "ai_invoice_text.json"

#     with open(output_file, "w", encoding="utf-8") as f:

#         json.dump(text_blocks, f, indent=4)

#     print("\nAI Extraction Completed")
#     print("Saved at:", output_file)


# # ---------------------------------------------------
# # MAIN PIPELINE
# # ---------------------------------------------------

# if __name__ == "__main__":

#     try:

#         print("===================================")
#         print("AI INVOICE STRUCTURE EXTRACTION")
#         print("===================================\n")

#         invoice = get_latest_invoice()

#         print("Processing Invoice:", invoice)

#         # ---------------------------
#         # PDF Handling
#         # ---------------------------

#         if invoice.suffix.lower() == ".pdf":

#             images = convert_pdf_to_images(invoice)

#         else:

#             images = [str(invoice)]

#         print("\nTotal pages detected:", len(images))

#         all_blocks = []

#         # ---------------------------
#         # PROCESS EACH PAGE
#         # ---------------------------

#         for img in images:

#             print("\nProcessing page:", img)

#             results = process_image(img)

#             blocks = extract_text_blocks(results)

#             all_blocks.extend(blocks)

#         # ---------------------------
#         # CLEAN OUTPUT
#         # ---------------------------

#         cleaned = clean_text_blocks(all_blocks)

#         # ---------------------------
#         # SAVE OUTPUT
#         # ---------------------------

#         save_ai_output(cleaned)

#         print("\nTotal blocks extracted:", len(cleaned))

#         print("\nAI Extraction Finished Successfully\n")

#     except Exception as e:

#         print("\nFatal Error in AI extraction\n")

#         print(e)

#         traceback.print_exc()





from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "invoices" / "raw"
OUTPUT_DIR = BASE_DIR / "output" / "ai_extraction"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_latest_invoice():

    files = list(INPUT_DIR.glob("*"))

    if not files:
        raise Exception("No invoice found")

    latest = max(files, key=lambda x: x.stat().st_mtime)

    return latest


if __name__ == "__main__":

    invoice = get_latest_invoice()

    metadata = {
        "file_name": invoice.name,
        "file_path": str(invoice),
        "file_type": invoice.suffix.lower()
    }

    output_file = OUTPUT_DIR / "invoice_metadata.json"

    with open(output_file, "w") as f:
        json.dump(metadata, f, indent=4)

    print("Invoice metadata prepared")