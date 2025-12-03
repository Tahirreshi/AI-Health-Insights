import fitz 

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text if text.strip() else "No text found in PDF."
    except:
        return "Error reading PDF file."
