import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from utils.ocr_handler import extract_text_from_image
from utils.pdf_handler import extract_text_from_pdf
from utils.table_formatter import extract_table, convert_to_table, filter_abnormal
from utils.groq_ai import get_health_advice, get_health_tip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.jfif', '.webp')


@app.route("/")
def home():
    tip = get_health_tip() or "Stay healthy and hydrated!"
    return render_template("index.html", tip=tip)


@app.route("/get-tip")
def get_tip():
    tip = get_health_tip() or "Move your body today — even gentle stretching helps."
    return jsonify({"tip": tip})


@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded = request.files.get('file')
    if not uploaded:
        return "No file uploaded", 400

    # Save file
    filename = secure_filename(uploaded.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded.save(filepath)

    mime = (uploaded.mimetype or "").lower()
    ext = os.path.splitext(filename)[1].lower()

    # Extract text
    if mime.startswith("image/") or ext in IMG_EXTENSIONS:
        text_data = extract_text_from_image(filepath)
    elif mime == "application/pdf" or ext == ".pdf":
        text_data = extract_text_from_pdf(filepath)
    else:
        text_data = f"Unsupported file format: {mime} / {ext}"

    # AI advice
    advice = get_health_advice(text_data)

    # Table extraction
    rows = extract_table(text_data)
    table = convert_to_table(rows)
    abnormal_table = filter_abnormal(table)

    final_table = abnormal_table if abnormal_table else []

    return render_template(
        "result.html",
        extracted=text_data,
        table=final_table,
        advice=advice
    )


if __name__ == "__main__":
    app.run(debug=True)
