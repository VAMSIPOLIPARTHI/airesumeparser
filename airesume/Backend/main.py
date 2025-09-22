from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

# Load Gemini API key from environment variable
genai.api_key = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Set your deployed frontend URL
FRONTEND_URL = "https://your-frontend-url.vercel.app"  # <-- Replace with your actual frontend URL

# Enable CORS only for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class EnhanceRequest(BaseModel):
    section: str
    content: str

class Resume(BaseModel):
    name: str
    experience: str
    education: str
    skills: str

# Temporary in-memory storage for resumes
resume_storage = {}

# Endpoint to enhance resume sections using Gemini
@app.post("/ai-enhance")
async def ai_enhance(request: EnhanceRequest):
    try:
        response = genai.chat.create(
            model="gemini-1.5-t",
            messages=[
                {"role": "system", "content": "You are an expert resume editor. Enhance the following content for clarity, professionalism, and impact."},
                {"role": "user", "content": request.content}
            ],
            temperature=0.7
        )
        enhanced_content = response.last.message.content
        return {"enhanced_content": enhanced_content}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to save the complete resume
@app.post("/save-resume")
async def save_resume(resume: Resume):
    resume_storage["resume"] = resume.dict()
    return {"status": "Resume saved successfully"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI backend is running. Visit /docs for API documentation."}
