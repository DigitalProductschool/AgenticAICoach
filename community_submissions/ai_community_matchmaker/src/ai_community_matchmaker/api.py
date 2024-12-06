from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.ai_community_matchmaker.crew import AiCommunityMatchmaker
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

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

        # Ensure the report exists
        if not os.path.exists(report_path):
            raise HTTPException(status_code=500, detail="The report file was not generated.")

        # Clean up temporary files
        os.remove(csv_path)
        os.remove(json_path)

        # Return the report file as a response
        return FileResponse(path=report_path, filename="report.md", media_type="text/markdown")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))