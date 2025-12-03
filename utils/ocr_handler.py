import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def extract_text_from_image(path):
    try:
        # Load image
        img = Image.open(path)

        # Convert to grayscale
        img = img.convert("L")

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)   # 2× stronger contrast

        # Increase sharpness
        sharpener = ImageEnhance.Sharpness(img)
        img = sharpener.enhance(2.0)

        # Resize → Tesseract works best on larger images
        width, height = img.size
        if width < 1500:  
            factor = 1500 / width
            img = img.resize((int(width * factor), int(height * factor)))

        # Optional slight blur (helps with noise)
        img = img.filter(ImageFilter.MedianFilter())

        # Run OCR
        text = pytesseract.image_to_string(
            img,
            config="--psm 6 -c preserve_interword_spaces=1"
        )

        return text if text.strip() else "No readable text found."

    except Exception as e:
        return f"OCR Error: {str(e)}"
