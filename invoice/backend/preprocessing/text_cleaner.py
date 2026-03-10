import re
from pathlib import Path

INPUT_DIR = Path("../../output/extracted_text")
OUTPUT_DIR = Path("../../output/cleaned_text")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_line(line: str) -> str:
    line = line.lower()

    # Common OCR corrections
    replacements = {
        "arnount": "amount",
        "totai": "total",
        "soid": "sold",
        "amaz0n": "amazon",
        "/-": "",
        "|": " ",
    }

    for wrong, correct in replacements.items():
        line = line.replace(wrong, correct)

    # Keep numbers, %, and words
    line = re.sub(r"[^a-z0-9.% ]", " ", line)

    # Normalize spaces INSIDE the line
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def clean_text(raw_text: str) -> str:
    cleaned_lines = []

    for line in raw_text.splitlines():
        clean = clean_line(line)
        if clean:  # skip empty lines
            cleaned_lines.append(clean)

    return "\n".join(cleaned_lines)


if __name__ == "__main__":
    input_file = INPUT_DIR / "invoice_text.txt"

    raw_text = input_file.read_text(encoding="utf-8")

    cleaned_text = clean_text(raw_text)

    output_file = OUTPUT_DIR / "cleaned_invoice_text.txt"
    output_file.write_text(cleaned_text, encoding="utf-8")

    print("✅ STRUCTURED TEXT CLEANING COMPLETED")
    print("📄 Cleaned structured text saved at:", output_file)
