# AI Pitch Coach (CrewAI)

AI Pitch Coach is a warm, step-by-step guide for founders to craft an investor-ready pitch. It supports three modes: structured coaching, message refinement, and investor Q&A simulation. Sessions are persisted in SQLite for iterative refinement.

## Run locally
```bash
cd community_submissions/coach_pitch_coach
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.pitch_coach.api:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## Example requests
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
   - `OPENAI_MODEL` (optional, defaults set in Render blueprint)
4. Deploy. The app will be available at `/docs` for Swagger UI.

## Screenshot / video instructions
For your demo assets:
1. Open Swagger UI at `/docs`.
2. Run a `POST /coach` request in each mode.
3. Capture screenshots of the request/response and a short video walkthrough.

