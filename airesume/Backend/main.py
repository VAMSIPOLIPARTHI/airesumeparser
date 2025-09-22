from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhanceRequest(BaseModel):
    section: str
    content: str

class Resume(BaseModel):
    name: str
    experience: str
    education: str
    skills: str

resume_storage = {}

@app.post("/ai-enhance")
async def ai_enhance(request: EnhanceRequest):
    enhanced_content = request.content + " (Enhanced by AI)"
    return {"enhanced_content": enhanced_content}

@app.post("/save-resume")
async def save_resume(resume: Resume):
    resume_storage["resume"] = resume.dict()
    return {"status": "Resume saved successfully"}

@app.get("/")
async def root():
    return {"message": "FastAPI backend is running. Visit /docs for API documentation."}

