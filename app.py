from flask import Flask, render_template, request, session, jsonify
import os
import json
import re

from utils.ocr_handler import extract_text
from utils.groq_ai import analyze_report, chat_with_doctor

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]

    if not file:
        return "No file uploaded"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Extract text
    extracted_text = extract_text(filepath)
    print("TEXT:\n", extracted_text)

    # Save for chat
    session["report_text"] = extracted_text

    # AI Analysis
    ai_result = analyze_report(extracted_text)
    print("AI RAW:\n", ai_result)

    # Extract JSON safely
    try:
        json_text = re.search(r"\{.*\}", ai_result, re.DOTALL)
        data = json.loads(json_text.group())
    except:
        return "AI response parsing failed"

    table = data.get("parameters", [])
    advice = data.get("advice", "")

    return render_template("result.html", table=table, advice=advice)


@app.route("/chat", methods=["POST"])
def chat():
    question = request.form["question"]
    report_text = session.get("report_text", "")

    if not report_text:
        return jsonify({"response": "Upload report first."})

    reply = chat_with_doctor(report_text, question)

    return jsonify({"response": reply})


if __name__ == "__main__":
    app.run(debug=True)