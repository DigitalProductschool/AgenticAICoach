import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .crew import GrowthHackingCrew
import logging

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger("growth_hacking_coach.api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Growth Hacking & Viral Marketing Coach API",
    description="AI-powered growth hacking and viral marketing coaching through conversational interface",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request/response
class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    message: str
    conversation_history: list[Message] = []

class QueryResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Growth Hacking & Viral Marketing Coach API"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        # Format conversation history for the crew
        formatted_history = ""
        if request.conversation_history:
            for msg in request.conversation_history:
                formatted_history += f"{msg.role.upper()}: {msg.content}\n\n"

        # Prepare inputs for the crew
        inputs = {
            'user_message': request.message,
            'conversation_history': formatted_history
        }

        logger.info(f'Processing request with conversation history of {len(request.conversation_history)} messages')

        # Create a crew instance and run it
        crew_instance = GrowthHackingCrew()
        logger.info(f'crew_instance created: {crew_instance}')
        crew = crew_instance.crew()
        logger.info(f'crew object: {crew}')
        result = crew.kickoff(inputs=inputs)
        logger.info(f'result from kickoff: {result}')

        # Extract the raw text from the result
        if hasattr(result, 'raw'):
            response_text = result.raw
        elif hasattr(result, 'tasks_output') and result.tasks_output:
            # Get the output from the first task
            response_text = result.tasks_output[0].raw
        else:
            response_text = str(result)

        return {"response": response_text}
    except Exception as e:
        logger.exception("Error in /query endpoint")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
