# ===== IMPORTS (all at the top) =====
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import anthropic
import json
import re
import io

# ===== CREATE APP =====
app = FastAPI()

# ===== FIX CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== YOUR CLAUDE API KEY =====
# IMPORTANT: Replace this with your real API key from console.anthropic.com
CLAUDE_API_KEY = "paste-your-real-api-key-here"

# ===== HEALTH CHECK =====
@app.get("/")
def home():
    return {"message": "Backend is running!"}


# ===== MAIN ANALYZE ENDPOINT =====
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form("")
):
    # STEP 1 - read the uploaded file
    file_bytes = await resume.read()

    # STEP 2 - extract text
    resume_text = extract_text_from_pdf(file_bytes)

    if not resume_text:
        return {"error": "Could not read the file. Please try another file."}

    # STEP 3 - send to Claude AI
    result = analyze_with_claude(resume_text, jobDescription)

    # STEP 4 - return result to frontend
    return result


# ===== FUNCTION TO READ FILE =====
def extract_text_from_pdf(file_bytes):

    # first try reading as PDF
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        if text.strip():
            print("Read as PDF successfully")
            return text
    except Exception as e:
        print("PDF read failed:", e)

    # if PDF fails try reading as plain text
    try:
        text = file_bytes.decode('utf-8')
        if text.strip():
            print("Read as TXT successfully")
            return text
    except Exception as e:
        print("TXT read failed:", e)

    # if both fail
    print("Could not read file at all")
    return None


# ===== FUNCTION TO CALL CLAUDE AI =====
def analyze_with_claude(resume_text, job_description):
    try:
        # create claude client
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        # build the prompt
        prompt = f"""
        You are an expert resume reviewer and career coach.

        Analyze the resume below and return ONLY a JSON object.
        No extra text, no markdown, no code blocks, just raw JSON.

        Resume:
        {resume_text}

        Job Description:
        {job_description if job_description else "No job description provided"}

        Return this exact JSON format:
        {{
            "score": <number between 0 and 100>,
            "strengths": ["strength 1", "strength 2", "strength 3"],
            "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
            "keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4"]
        }}
        """

        # call claude
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # get the response text
        response_text = message.content[0].text
        print("Claude returned:", response_text)

        # clean markdown if present
        response_text = response_text.strip()
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        # find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            print("Parsed successfully:", result)
            return result
        else:
            raise ValueError("No JSON found in Claude response")

    except Exception as e:
        print("Claude error:", e)
        # return mock data if something goes wrong
        return {
            "score": 70,
            "strengths": ["Good structure", "Clear experience", "Relevant skills"],
            "weaknesses": ["Missing summary", "No metrics", "Weak keywords"],
            "keywords": ["Python", "React", "Agile", "REST API"]
        }