from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from cv_reviewer.app.analyzer import analyze_cv
import os

app = FastAPI()

# Directory for saving intermediate reports
OUTPUT_DIR = "./cache/output"
UPLOAD_DIR = "./cache/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/analyze/")
async def analyze_endpoint(
    cv_file: UploadFile,
    job_description: str = Form(None)
):
    """
    Analyze a CV and optional job description.
    
    :param cv_file: The uploaded CV file.
    :param job_description: The optional job description text.
    :return: JSON response with a message and the result summary.
    """
    # Save the uploaded file to the uploads directory
    file_path = os.path.join(UPLOAD_DIR, cv_file.filename)
    with open(file_path, "wb") as f:
        content = await cv_file.read()
        f.write(content)
    try:
        # Analyze the CV
        result = analyze_cv(file_path, job_description)
        return JSONResponse(content={"status": "success", "result": result})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/{task_name}")
async def get_task_output(task_name: str):
    """
    Retrieve a saved report by task name.

    :param task_name: The name of the task (e.g., 'structure', 'relevance').
    :return: The saved report file.
    """
    file_path = os.path.join(OUTPUT_DIR, f"{task_name}.md")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/markdown")
    return JSONResponse(content={"status": "error", "message": f"{task_name} not found"}, status_code=404)
