from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from crew import crew, implement_gamification, research_task
import re

app = FastAPI(title="Environmental AI Coach API")


def process_input(location, user_input, user_points=0):
    if not location or not user_input:
        return "Error: Both fields are required.", "", "", "", user_points, "", ""

    try:
        inputs = {"user_input": user_input, "location": location}
        result = crew.kickoff(inputs)

        # Retrieve outputs for different steps
        research = research_task.output.raw
        gamification = implement_gamification.output.raw

        # Extract PM2.5 and PM10 values
        pm25 = "N/A"
        pm10 = "N/A"
        for line in research.split('\n'):
            if "PM2.5" in line:
                matches = re.findall(r"PM2.5:?\s*([-+]?\d*\.?\d+)", line)
                if matches:
                    pm25 = matches[0]
            if "PM10" in line:
                matches = re.findall(r"PM10:?\s*([-+]?\d*\.?\d+)", line)
                if matches:
                    pm10 = matches[0]

        quiz_question = ""
        options = []
        correct_answer = ""

        if "---QUIZ---" in gamification and "---END---" in gamification:
            quiz_content = gamification.split("---QUIZ---")[1].split("---END---")[0].strip()
            for line in quiz_content.split('\n'):
                line = line.strip()
                if line.startswith('QUESTION:'):
                    quiz_question = line.replace('QUESTION:', '').strip()
                elif line.startswith(('a)', 'b)', 'c)', 'd)')):
                    options.append(line)
                elif line.startswith('ANSWER:'):
                    correct_answer = line.replace('ANSWER:', '').strip().lower()

        return research, quiz_question, options, user_points, correct_answer, pm25, pm10

    except Exception as e:
        return f"Error occurred: {e}", "", "", "", user_points, "", "", ""
    
# Function to handle quiz answer
def handle_quiz_answer(user_answer, correct_answer, user_points):
    if user_answer.lower() == correct_answer:
        user_points += 1
        feedback = f"Correct! You earned 1 point. Total points: {user_points}"
    else:
        feedback = f"Incorrect. The correct answer was '{correct_answer}'. Total points: {user_points}"
    return feedback, user_points

class UserInput(BaseModel):
    location: str
    user_input: str
    user_points: Optional[int] = 0

class QuizAnswer(BaseModel):
    user_answer: str
    correct_answer: str
    user_points: int

class EnvironmentalResponse(BaseModel):
    research: str
    quiz_question: str
    quiz_options: List[str]
    user_points: int
    correct_answer: str
    pm25: str
    pm10: str

@app.post("/environmental-advice", response_model=EnvironmentalResponse)
async def get_environmental_advice(user_input: UserInput):
    try:
        research, quiz_question, options, points, correct_answer, pm25, pm10 = process_input(
            user_input.location,
            user_input.user_input,
            user_input.user_points
        )
        
        return EnvironmentalResponse(
            research=research,
            quiz_question=quiz_question,
            quiz_options=options,
            user_points=points,
            correct_answer=correct_answer,
            pm25=pm25,
            pm10=pm10
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz-answer")
async def submit_quiz_answer(quiz_input: QuizAnswer):
    try:
        feedback, points = handle_quiz_answer(
            quiz_input.user_answer,
            quiz_input.correct_answer,
            quiz_input.user_points
        )
        return {"feedback": feedback, "points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))