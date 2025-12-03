import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_health_advice(text):
    try:
        prompt = f"""
        You are a medical expert. Analyze this extracted health report text and 
        provide safe, simple, clear advice. Do NOT give medication, diagnosis, or 
        harmful instructions.

        Report:
        {text}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.5
        )

        if not response or not response.choices:
            return "Unable to analyze the report, but staying healthy includes hydration, sleep, and balanced meals."

        advice = response.choices[0].message.content
        return advice.strip() if advice else "Keep up healthy habits!"

    except Exception as e:
        print("\n--- HEALTH ADVICE ERROR ---\n", e)
        return "Unable to process the report — but remember to drink water and rest well."


def get_health_tip():
    try:
        prompt = "Give one short, unique, actionable health tip (under 15 words)."

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=1.0
        )

        if not response or not response.choices:
            return "Move for 2 minutes — your body will thank you."

        tip = response.choices[0].message.content

        return tip.strip() if isinstance(tip, str) else "Take a deep breath — it relaxes your nervous system."

    except Exception as e:
        print("\n--- HEALTH TIP ERROR ---\n", e)
        return "Take short stretch breaks every hour."
