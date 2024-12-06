from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.responses import HTMLResponse
from src.ai_community_matchmaker.crew import AiCommunityMatchmaker
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>AiCommunityMatchmaker</title>
        </head>
        <body>
            <h1>Welcome to Ai Community Matchmaker!</h1>
            <p>
                <a href="/docs">Go to API Documentation (Swagger UI)</a>
            </p>
        </body>
    </html>
    """

@app.post("/run-matchmaker/")
async def run_matchmaker(
    csv_file: UploadFile = File(...),
    target_user_file: UploadFile = File(...)
):
    """
    Run the Community Matchmaker with uploaded CSV and JSON files.
    """
    try:
        # Save uploaded files temporarily
        csv_path = "./src/ai_community_matchmaker/data/temp_community.csv"
        json_path = "./src/ai_community_matchmaker/data/temp_target_user.json"
        report_path = "output/report.md"
        
        with open(csv_path, "wb") as f:
            f.write(await csv_file.read())
        with open(json_path, "wb") as f:
            f.write(await target_user_file.read())

        # Run the CrewAI process
        inputs = {
            'target_user': json_path,
            'community_members': csv_path,
        }
        result = AiCommunityMatchmaker().crew().kickoff(inputs=inputs)
        
        # Clean up temporary files
        os.remove(csv_path)
        os.remove(json_path)
        
        # Read the contents of the Markdown file into result_text
        with open(report_path, "r") as md_file:
            result_text = md_file.read()

        print(f"Report content: {result_text}")
        # Return both the file download link and the textual result
        return {
            "message": "Matchmaker executed successfully",
            "result_summary": result_text,
            "download_link": f"/download-report/",
        }
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))    
        
@app.get("/download-report/")
async def download_report():
    md_file_path = "output/report.md"
    if os.path.exists(md_file_path):
        return FileResponse(md_file_path, media_type="text/markdown", filename="report.md")
    return JSONResponse({"error": "Report file not found"}, status_code=404)