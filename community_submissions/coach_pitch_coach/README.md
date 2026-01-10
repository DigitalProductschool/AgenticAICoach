# AI Pitch Coach (CrewAI)

AI Pitch Coach is a warm, step-by-step guide for founders to craft an investor-ready pitch. It supports three modes: structured coaching, message refinement, and investor Q&A simulation. Sessions are persisted in SQLite for iterative refinement.

## Live Demo on Render

**Try it now:** [https://ai-pitch-coach-0z0m.onrender.com](https://ai-pitch-coach-0z0m.onrender.com)  
**API Documentation:** [https://ai-pitch-coach-0z0m.onrender.com/docs](https://ai-pitch-coach-0z0m.onrender.com/docs)

## Features

✨ **Interactive Web UI** - Beautiful chat interface with real-time progress tracking  
📊 **Progress Visualization** - See your pitch development across 10 stages  
🎯 **Three Coaching Modes** - Coach, Refine, and Q&A with intelligent AI agents  
💾 **Session Persistence** - Continue where you left off with SQLite storage  
📈 **Real-time Scoring** - Get clarity, persuasion, and confidence scores  
📝 **Markdown Support** - Beautifully formatted responses with proper styling  
🚀 **Export Pitches** - Download your completed pitch as Markdown

## Run locally
```bash
cd community_submissions/coach_pitch_coach
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
uvicorn src.pitch_coach.api:app --reload --port 8000
```

**Open the Web UI:** `http://127.0.0.1:8000`  
**Or access Swagger API docs:** `http://127.0.0.1:8000/docs`

## Run with Docker

The easiest way to deploy the application is using Docker:

### Build and Run
```bash
cd community_submissions/coach_pitch_coach

# Build the Docker image
docker build -t pitch-coach-api .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -e OPENAI_MODEL=gpt-4o-mini \
  pitch-coach-api
```

### With Persistent Database
To persist session data between container restarts:

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -e OPENAI_MODEL=gpt-4o-mini \
  -v $(pwd)/db:/app/db \
  pitch-coach-api
```

### Access the Application
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Using the Web Interface

The Web UI provides an intuitive chat experience:

1. **Select a Mode:**
   - 🎓 **Coach** - Step-by-step guidance through 10 pitch stages
   - ✨ **Refine** - Polish your existing pitch text
   - 💬 **Q&A** - Practice investor questions

2. **Configure Settings:**
   - Choose your audience (VC, Angel, Accelerator, Corporate)
   - Select funding stage (Pre-seed, Seed, Series A, B+)
   - Add industry for Q&A mode

3. **Chat with the Coach:**
   - Type your responses in the input area
   - See real-time progress in Coach mode
   - Get instant scoring feedback
   - Export your completed pitch

4. **Session Management:**
   - Sessions auto-save to continue later
   - Start new sessions anytime
   - Export pitches as Markdown files

## API Endpoints

For programmatic access, the API provides these endpoints:

- `GET /` - Redirects to Web UI
- `GET /health` - Health check
- `POST /coach` - Main coaching endpoint (all modes)
- `GET /sessions/{session_id}` - Retrieve session data

## Example API requests

Coach mode (step-by-step):
```bash
curl -X POST http://127.0.0.1:8000/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "coach",
    "user_message": "We help CFOs close the books in hours instead of days.",
    "audience": "VC",
    "funding_stage": "pre-seed"
  }'
```

Refine mode (rewrite and improve):
```bash
curl -X POST http://127.0.0.1:8000/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "refine",
    "user_message": "Our product uses AI to make finance teams more efficient.",
    "audience": "VC",
    "funding_stage": "seed"
  }'
```

Investor Q&A mode:
```bash
curl -X POST http://127.0.0.1:8000/coach \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "qa",
    "user_message": "We automate monthly close for mid-market SaaS companies.",
    "industry": "FinTech",
    "audience": "VC",
    "funding_stage": "seed"
  }'
```

## Deploy on Render
1. Create a new Render Web Service and connect the repo.
2. Use:
   - Root Directory: `community_submissions/coach_pitch_coach`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.pitch_coach.api:app --host 0.0.0.0 --port 10000`
3. Add environment variables:
   - `OPENAI_API_KEY` (required)
   - `OPENAI_MODEL` (optional, defaults to gpt-4o-mini)
4. Deploy. The app will be available at your Render URL.

## Project Structure

```
community_submissions/coach_pitch_coach/
├── src/
│   └── pitch_coach/
│       ├── api.py              # FastAPI application
│       ├── crew.py             # CrewAI agent orchestration
│       ├── config/
│       │   ├── agents.yaml     # Agent definitions
│       │   └── tasks.yaml      # Task definitions
│       └── tools/
│           ├── storage.py      # SQLite session management
│           ├── stage_router.py # Pitch stage progression
│           └── scoring.py      # Heuristic text scoring
├── static/
│   ├── index.html              # Web UI
│   ├── css/styles.css          # Styling
│   └── js/app.js               # Frontend logic
├── tests/
│   ├── conftest.py
│   └── test_api.py             # API endpoint tests
├── requirements.txt
├── render.yaml                 # Render deployment config
└── README.md
```

## Tech Stack

- **Backend**: FastAPI, CrewAI, LangChain
- **AI**: OpenAI GPT-4o-mini
- **Database**: SQLite
- **Frontend**: Vanilla JS, Marked.js (markdown parsing)
- **Deployment**: Render

## Demo Screenshots

### Web UI
The interactive chat interface guides founders through pitch development with real-time progress tracking and scoring.

### Server & API Documentation
- **`server_running.png`** - FastAPI server running successfully on port 8000
- **`swagger_ui.png`** - Full Swagger/OpenAPI documentation showing all endpoints
- **`health_endpoint.png`** - Health check endpoint returning 200 OK status

### API Endpoint Tests
- **`coach_endpoint.png`** - POST /coach endpoint test in Swagger UI
- **`1_coach_mode_request_response.png`** - Coach mode: Step-by-step pitch structuring
- **`2_refine_mode_request_response.png`** - Refine mode: Polish and improve pitch text
- **`3_qa_mode_request_response.png`** - Q&A mode: Practice investor questions

### Web Interface
- **`app_home_page.png`** - Interactive web UI with chat interface, mode selector, and real-time progress tracking

All screenshots show successful 200 responses with proper JSON formatting, demonstrating full functionality across all three coaching modes (Coach, Refine, Q&A).

---

**Built with CrewAI and OpenAI**

