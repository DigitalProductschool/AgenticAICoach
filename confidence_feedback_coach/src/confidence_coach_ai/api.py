from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from crew import crew, analyze_communication_task, summarize_analyzer_output_task, provide_feedback_task
from tools.custom_tool import AudioTranscriberTool

app = FastAPI()

class UserInput(BaseModel):
    message: str
    is_first_submission: bool = True

class AnalysisResponse(BaseModel):
    turn: int
    analysis: str
    summary: str
    feedback: str

class ChatHistory(BaseModel):
    history: List[AnalysisResponse] = []

# Global chat history store (in production, use a proper database)
chat_histories = {}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_message(user_input: UserInput, session_id: str):
    try:
        # Initialize chat history for new sessions
        if session_id not in chat_histories:
            chat_histories[session_id] = ChatHistory()
        
        chat_history = chat_histories[session_id]
        current_turn = len(chat_history.history) + 1

        # Handle audio input if needed
        message = user_input.message
        if message.lower().endswith(('.mp3', '.wav')):
            transcriber = AudioTranscriberTool()
            message = transcriber.run(message)

        # Process with crew
        inputs = {"text": message, "is_first_submission": user_input.is_first_submission}
        result = crew.kickoff(inputs)

        # Get outputs
        analysis = analyze_communication_task.output.raw
        summary = summarize_analyzer_output_task.output.raw
        feedback = provide_feedback_task.output.raw

        response = AnalysisResponse(
            turn=current_turn,
            analysis=analysis,
            summary=summary,
            feedback=feedback
        )

        # Store in chat history
        chat_history.history.append(response)
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}", response_model=ChatHistory)
async def get_chat_history(session_id: str):
    if session_id not in chat_histories:
        return ChatHistory()
    return chat_histories[session_id] 