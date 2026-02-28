# ResumeAI – AI-Powered Resume Analyzer

ResumeAI is a full-stack web application that analyzes resumes using AI and provides actionable feedback in seconds.

It evaluates resumes against a job description and generates:

- Overall Score (0–100)
- Key Strengths
- Areas for Improvement
- Missing Keywords

Built as a solo hackathon project.

---

## 🚀 Problem Statement

Many students and job seekers apply to jobs without knowing whether their resume matches the job description.

They often receive rejections without understanding:
- What is missing?
- Which skills are weak?
- How strong their resume actually is?

There is a need for instant, intelligent resume feedback.

---

## 💡 Solution

ResumeAI allows users to:

1. Upload their resume (PDF / DOCX / TXT)
2. Paste a job description (optional)
3. Receive AI-powered feedback instantly

The system:
- Extracts text from the resume
- Sends it to Claude AI for analysis
- Returns structured JSON results
- Displays a clean, modern UI with categorized feedback

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3 (Dark modern UI)
- Vanilla JavaScript (Fetch API)

### Backend
- FastAPI (Python)
- pdfplumber (PDF text extraction)
- Anthropic Claude API (AI analysis)

### Architecture
Frontend → FastAPI Backend → Claude AI → JSON Response → UI Rendering

---

## ⚙️ How It Works

1. User uploads resume.
2. JavaScript sends resume + job description as FormData.
3. FastAPI:
   - Extracts resume text.
   - Builds structured AI prompt.
   - Sends prompt to Claude.
4. Claude returns structured JSON:
   ```json
   {
     "score": 78,
     "strengths": [],
     "weaknesses": [],
     "keywords": []
   }
