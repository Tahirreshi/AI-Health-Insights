import fitz
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        text = ""

        for page in doc:
            page_text = page.get_text()

            # If normal text exists
            if page_text.strip():
                text += page_text
            else:
                # 🔥 OCR fallback (for scanned PDFs)
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                text += pytesseract.image_to_string(img)

        return text if text.strip() else "No text found in PDF."

    except Exception as e:
        print("\nPDF ERROR:", e)
        return f"PDF Error: {str(e)}"