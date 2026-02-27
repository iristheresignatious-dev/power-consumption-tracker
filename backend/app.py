
# ===== IMPORTS =====
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import anthropic
import json
import io

# ===== CREATE APP =====
app = FastAPI()

# ===== FIX CORS (allows frontend to talk to backend) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== YOUR CLAUDE API KEY =====
CLAUDE_API_KEY = "paste-your-api-key-here"

# ===== HEALTH CHECK (test if server is running) =====
@app.get("/")
def home():
    return {"message": "Backend is running!"}


# ===== MAIN ANALYZE ENDPOINT =====
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form("")
):

    # STEP 1 - read the uploaded PDF file
    file_bytes = await resume.read()

    # STEP 2 - extract text from PDF
    resume_text = extract_text_from_pdf(file_bytes)

    if not resume_text:
        return {"error": "Could not read the PDF. Please try another file."}

    # STEP 3 - send to Claude AI and get analysis
    result = analyze_with_claude(resume_text, jobDescription)

    # STEP 4 - return result to frontend
    return result


# ===== FUNCTION TO READ PDF =====
def extract_text_from_pdf(file_bytes):
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print("PDF error:", e)
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
        No extra text, just the JSON.
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description if job_description else "No job description provided"}
        
        Return this exact JSON format:
        {{
            "score": <number between 0 and 100>,
            "strengths": [<list of 3 strengths as strings>],
            "weaknesses": [<list of 3 weaknesses as strings>],
            "keywords": [<list of 4 missing keywords as strings>]
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

        # convert to python dictionary
        result = json.loads(response_text)
        return result

    except Exception as e:
        print("Claude error:", e)
        # return mock data if something goes wrong
        return {
            "score": 70,
            "strengths": ["Good structure", "Clear experience", "Relevant skills"],
            "weaknesses": ["Missing summary", "No metrics", "Weak keywords"],
            "keywords": ["Python", "React", "Agile", "REST API"]
        }