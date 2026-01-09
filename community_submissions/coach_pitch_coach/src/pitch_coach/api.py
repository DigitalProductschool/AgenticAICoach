from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
import uuid

from .crew import build_crew, run_structure, run_refine, run_qa
from .tools.storage import get_or_create_session, save_session, add_message
from .tools.stage_router import next_stage, STAGE_QUESTIONS
from .tools.scoring import score_text

app = FastAPI(title="AI Pitch Coach", version="0.1.0")

crew_parts = None

class CoachRequest(BaseModel):
  session_id: Optional[str] = None
  mode: Literal["coach", "refine", "qa"] = "coach"

  user_message: str = Field(..., min_length=1)

  audience: str = "VC"
  funding_stage: str = "pre-seed"
  industry: Optional[str] = None

class CoachResponse(BaseModel):
  session_id: str
  mode: str
  stage: Optional[str] = None
  coach_response: str
  next_question: Optional[str] = None
  scores: Optional[Dict[str, int]] = None
  context: Optional[Dict[str, Any]] = None

@app.on_event("startup")
def startup():
  global crew_parts
  crew_parts = build_crew()

@app.get("/health")
def health():
  return {"ok": True}

@app.post("/coach", response_model=CoachResponse)
def coach(req: CoachRequest):
  session_id = req.session_id or str(uuid.uuid4())
  state = get_or_create_session(session_id)

  add_message(session_id, "user", req.user_message, meta={"mode": req.mode})

  # Scores always returned for user_message (simple heuristic)
  scores = score_text(req.user_message)

  if req.mode == "qa":
    industry = req.industry or "AI / Software"
    pitch_summary = state.context.get("last_refined_pitch") or req.user_message
    result = run_qa(crew_parts, industry=industry, funding_stage=req.funding_stage, pitch_summary=pitch_summary, audience=req.audience)
    coach_text = str(result)
    add_message(session_id, "assistant", coach_text, meta={"mode": "qa"})
    return CoachResponse(session_id=session_id, mode="qa", coach_response=coach_text, scores=scores, context=state.context)

  if req.mode == "refine":
    result = run_refine(crew_parts, pitch_text=req.user_message, audience=req.audience, funding_stage=req.funding_stage)
    coach_text = str(result)
    state.context["last_refined_pitch"] = coach_text
    save_session(state)
    add_message(session_id, "assistant", coach_text, meta={"mode": "refine"})
    return CoachResponse(session_id=session_id, mode="refine", coach_response=coach_text, scores=scores, context=state.context)

  # mode == "coach": step-by-step pitch structuring
  current_stage = state.stage
  # store the user's answer into the current stage field
  state.context[current_stage] = req.user_message

  # run coaching step for current stage
  result = run_structure(
    crew_parts,
    stage=current_stage,
    context=state.context,
    user_message=req.user_message,
    audience=req.audience,
    funding_stage=req.funding_stage,
  )
  coach_text = str(result)

  # advance stage
  state.stage = next_stage(current_stage)
  save_session(state)

  next_q = STAGE_QUESTIONS.get(state.stage)

  add_message(session_id, "assistant", coach_text, meta={"mode": "coach", "stage": current_stage})

  return CoachResponse(
    session_id=session_id,
    mode="coach",
    stage=current_stage,
    coach_response=coach_text,
    next_question=next_q,
    scores=scores,
    context=state.context,
  )