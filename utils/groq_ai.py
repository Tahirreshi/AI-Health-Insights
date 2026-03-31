from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------- ANALYZE REPORT ----------
def analyze_report(text):
    prompt = f"""
You are a medical AI.

Analyze the lab report and return ONLY valid JSON.

Format:
{{
  "parameters": [
    {{
      "name": "parameter",
      "value": number,
      "unit": "unit",
      "reference": "range",
      "status": "normal or abnormal"
    }}
  ],
  "advice": "short medical advice"
}}

Lab Report:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------- CHAT WITH DOCTOR ----------
def chat_with_doctor(report_text, question):
    prompt = f"""
You are a helpful medical AI doctor.

Patient's lab report:
{report_text}

Patient question:
{question}

Answer clearly in simple language.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content