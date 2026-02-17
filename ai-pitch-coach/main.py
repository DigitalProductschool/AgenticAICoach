import os
import tempfile
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

from openai import OpenAI

# ==============================
# App Setup
# ==============================

app = FastAPI(title="AI Pitch Coach")

app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.4,
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.get("/", response_class=HTMLResponse)
async def home():
    return open("templates/index.html", encoding="utf-8").read()

current_dir = os.path.join(os.getcwd(), "tmp")
os.makedirs(current_dir, exist_ok=True)

@app.post("/get-transcription")
async def pitch(audio: UploadFile = File(...)):
    # Save uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, dir=current_dir, suffix=".webm") as tmp:
        tmp.write(await audio.read())
        
        audio_path = "./tmp/" + os.path.basename(tmp.name)
        print("audio_path: ", audio_path, flush=True)

        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe", 
                # model="whisper-1", 
                file=f,
                language="en",
                response_format="text"
            )

            user_text = transcription

        return {
            "transcript": user_text,
        }
    
pitch_improver_agent = Agent(
    role="Pitch Improvement Coach",
    goal=(
        "Rewrite user startup messages into clear, professional, investor-ready pitch language "
        "without changing the original meaning."
    ),
    backstory=(
        "You are an expert startup pitch editor. "
        "Founders often speak in messy, unstructured ways when recording voice notes. "
        "Your job is to polish their exact message into something concise, confident, "
        "and professional — while keeping the same idea and intent."
    ),
    verbose=True,
    llm=llm
)

def build_improvement_task(user_text: str):

    return Task(
        description=f"""
You are given a raw startup pitch transcription from a founder.

The text may be:
- unstructured
- too long
- repetitive
- unclear
- full of filler words
- slightly incorrect due to speech-to-text errors

Your job:

1. Rewrite the pitch in a more professional, investor-ready way.
2. Keep the EXACT same meaning and core idea.
3. Do NOT add new claims, features, or facts.
4. Make it clear, confident, and well-structured.
5. Output only the improved version (no explanations).

RAW USER TEXT:
\"\"\"{user_text}\"\"\"

Return the improved pitch below:
""",
        expected_output="A polished, professional improved version of the same pitch text.",
        agent=pitch_improver_agent
    )

def improve_pitch(user_text: str):

    task = build_improvement_task(user_text)

    crew = Crew(
        agents=[pitch_improver_agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return str(result)

@app.post("/improve")
async def improve(data: dict):

    user_text = data["text"]

    improved_text = improve_pitch(user_text)

    return {
        "improved": improved_text
    }

# ==============================
# CrewAI Agents
# ==============================

pitch_structure_agent = Agent(
    role="Pitch Structure Coach",
    goal="Help founders define problem, solution, and UVP step by step",
    backstory="A warm startup mentor helping founders craft investor-ready pitch structure.",
    llm=llm,
    verbose=True
)

messaging_agent = Agent(
    role="Pitch Messaging Expert",
    goal="Improve clarity, persuasiveness, and simplify AI concepts",
    backstory="Expert at translating complex AI ideas into simple investor language.",
    llm=llm,
    verbose=True
)

qa_agent = Agent(
    role="Investor Q&A Simulator",
    goal="Simulate tough investor questions and objections",
    backstory="Former VC partner who challenges founders with realistic questions.",
    llm=llm,
    verbose=True
)

iteration_agent = Agent(
    role="Pitch Iteration Coach",
    goal="Encourage resubmission and track improvement across revisions",
    backstory="Supportive pitch coach helping founders iterate confidently.",
    llm=llm,
    verbose=True
)

# ==============================
# Coaching Steps (Task Flow)
# ==============================

TASK_FLOW = [
    {
        "agent": pitch_structure_agent,
        "prompt": """
You are the Pitch Structure Coach.

Ask the founder ONE question:
- What is the core problem?
Be supportive and warm.
Wait for their reply.
"""
    },
    {
        "agent": pitch_structure_agent,
        "prompt": """
Great. Now ask ONE question:
- What is your AI solution and why is it unique?
Wait for reply.
"""
    },
    {
        "agent": messaging_agent,
        "prompt": """
Analyze the founder's pitch so far.

1. Give 2 actionable improvements on clarity + persuasiveness.
2. Rewrite their pitch in a stronger investor-friendly way.
Then ask: "Does this feel accurate?"
"""
    },
    {
        "agent": qa_agent,
        "prompt": """
Simulate ONE tough investor question based on the startup idea.
Make it realistic and challenging.
Wait for founder response.
"""
    },
    {
        "agent": qa_agent,
        "prompt": """
Give feedback on the founder’s answer:
- confidence
- conciseness
- strength

Then ask ONE follow-up investor objection.
Wait for reply.
"""
    },
    {
        "agent": iteration_agent,
        "prompt": """
Encourage iteration.

1. Highlight what improved.
2. Suggest the next pitch refinement.
Ask the founder to resubmit their updated pitch in one sentence.
"""
    }
]

# ==============================
# WebSocket Coaching Session
# ==============================

@app.websocket("/ws")
async def pitch_coach_ws(ws: WebSocket):
    await ws.accept()

    history = ""
    step = 0

    # ----------------------------
    # Receive startup pitch
    # ----------------------------
    init_data = await ws.receive_text()
    init_json = json.loads(init_data)

    startup = init_json["pitch"]

    history += f"\nFounder: {startup}\n"

    await ws.send_text("✅ Awesome — let’s build your pitch step by step!")

    # ----------------------------
    # Interactive Coaching Loop
    # ----------------------------
    while step < len(TASK_FLOW):

        current = TASK_FLOW[step]
        agent = current["agent"]

        # Build prompt with memory
        prompt = f"""
Conversation so far:
{history}

{current['prompt']}
"""
        
        task = Task(
            description=prompt,
            agent=agent,
            expected_output="A coaching response + one question."
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()
        agent_output = str(result)

        # Send agent message immediately
        await ws.send_text(json.dumps({
            "agent": agent.role,
            "message": agent_output
        }))

        # Save memory
        history += f"\nAgent ({agent.role}): {agent_output}\n"

        # Wait for user reply
        user_data = await ws.receive_text()
        user_json = json.loads(user_data)

        reply = user_json["reply"]
        history += f"\nFounder reply: {reply}\n"

        step += 1

    # Done
    await ws.send_text("🎉 Pitch coaching complete! Want to run another iteration?")
    await ws.close()
