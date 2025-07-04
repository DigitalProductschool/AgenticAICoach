import os
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from src.utils import file_parser, agent_helper

app = FastAPI(
    title="CV Review AI Coach API",
    description="An API for getting structured, AI-powered feedback on your CV.",
    version="3.0.0", # Final user-friendly version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.post("/review-cv")
def review_cv_endpoint(file: UploadFile = File(...)) -> Dict:
    """
    Accepts a CV file, parses it, runs the analysis crew, and returns a
    structured JSON object conforming to the CVReview Pydantic model.
    """
    filename = file.filename
    file_stream = BytesIO(file.file.read())
    
    try:
        if filename.endswith(".pdf"):
            content = file_parser.parse_pdf_text(file_stream)
        elif filename.endswith(".docx"):
            content = file_parser.parse_docx_text(file_stream)
        else:
            raise HTTPException(400, "Unsupported file type. Please upload a .pdf or .docx file.")
    except Exception as e:
        raise HTTPException(500, f"Failed to parse file: {e}")

    if not content.strip():
        raise HTTPException(400, "Could not extract text from the file.")

    unique_github_urls = file_parser.find_github_urls(content)

    try:
        crew_output = agent_helper.run_cv_review_crew(content, unique_github_urls)
        if not crew_output or not hasattr(crew_output, 'pydantic'):
             raise HTTPException(500, "Crew failed to produce a structured output.")
        return {"status": "success", "review": crew_output.pydantic.model_dump()}
    except Exception as e:
        raise HTTPException(500, f"An error occurred during AI processing: {e}")

# --- Static File Serving ---
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(static_dir, 'index.html'))
