from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_parsing import extract_text
from app.services.cv_analysis import analyze_cv

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a PDF or DOCX file.")

    # Read file content
    file_content = await file.read()

    # Extract text
    text = extract_text(file_content, file.content_type)
    if not text:
        raise HTTPException(status_code=500, detail="Failed to extract text from the file.")

    # Analyze the extracted text
    feedback = analyze_cv(text)

    return {
        "filename": file.filename,
        "feedback": feedback
    }
