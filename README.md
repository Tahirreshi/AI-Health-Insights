#  Smart Health Advisor (AI-Powered)

An intelligent web application that analyzes medical lab reports (PDF/Image) and provides structured insights, abnormal value detection, and personalized AI-driven health advice — with an interactive **AI Doctor Chat**.

---

##  Features

-  Upload lab reports (PDF / Image)
-  OCR-based text extraction
-  AI-powered report analysis (Groq LLM)
-  Structured parameter table
-  Abnormal value detection
-  Medical advice generation
-  Chat with AI Doctor (context-aware)
-  Clean and modern UI (Flask + Tailwind)

---

##  How It Works

1. User uploads a lab report
2. OCR extracts text from the report
3. AI analyzes the report and returns structured JSON:
   - Parameters
   - Values
   - Reference ranges
   - Status (Normal / Abnormal)
4. Results are displayed in a table
5. User can interact with AI Doctor for further queries

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **AI Model:** Groq LLM
- **OCR:** Tesseract + Pillow
- **PDF Parsing:** pdfplumber
- **Frontend:** HTML, Tailwind CSS
- **Version Control:** Git & GitHub


## 📂 Project Structure
