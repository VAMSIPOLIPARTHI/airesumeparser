from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import google.generativeai as genai

# Load Gemini API key from environment variable
genai.api_key = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Allowed frontend origins
origins = [
    "https://airesumeparser-one.vercel.app",  # deployed frontend
    "http://localhost:3000"                   # local dev
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class EnhanceRequest(BaseModel):
    section: Optional[str] = "unknown"
    content: Optional[str] = ""

class Resume(BaseModel):
    name: Optional[str] = ""
    experience: Optional[str] = ""
    education: Optional[str] = ""
    skills: Optional[str] = ""

# Temporary in-memory storage
resume_storage = {}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI backend is running. Visit /docs for API documentation."}

# Endpoint to enhance resume sections using Gemini
@app.post("/ai-enhance")
async def ai_enhance(request: EnhanceRequest):
    # Log incoming request for debugging
    print("Received request:", request.dict())

    # Validate input
    if not request.content or request.content.strip() == "":
        return {"error": f"No content provided for section '{request.section}'."}

    try:
        response = genai.chat.create(
            model="gemini-1.5-t",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume editor. Enhance the following content for clarity, professionalism, and impact."
                },
                {"role": "user", "content": request.content}
            ],
            temperature=0.7
        )
        enhanced_content = response.last.message.content
        return {"enhanced_content": enhanced_content}
    except Exception as e:
        return {"error": str(e)}

# Endpoint to save resume
@app.post("/save-resume")
async def save_resume(resume: Resume):
    # Log resume data
    print("Saving resume:", resume.dict())

    resume_storage["resume"] = resume.dict()
    return {"status": "Resume saved successfully"}
