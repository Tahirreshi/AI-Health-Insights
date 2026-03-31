import pytesseract
from PIL import Image
import pdfplumber
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
        return extract_from_image(file_path)

    elif ext == ".pdf":
        return extract_from_pdf(file_path)

    else:
        return "Unsupported file format"


def extract_from_image(path):
    img = Image.open(path).convert("L")
    text = pytesseract.image_to_string(img)
    return text


def extract_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text