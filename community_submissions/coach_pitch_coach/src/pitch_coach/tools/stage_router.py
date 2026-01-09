STAGES = [
  "one_liner",
  "problem",
  "solution",
  "uvp",
  "target_customer",
  "market",
  "business_model",
  "traction",
  "moat",
  "ask"
]

STAGE_QUESTIONS = {
  "one_liner": "In one sentence, what does your startup do and for whom?",
  "problem": "What painful problem are you solving (who feels it, how often, how costly)?",
  "solution": "What is your solution and how does it work at a high level (no jargon)?",
  "uvp": "What makes you meaningfully different from alternatives and competitors?",
  "target_customer": "Who is the ideal customer and who is the buyer vs user?",
  "market": "What market are you in and what’s the initial wedge / beachhead segment?",
  "business_model": "How do you make money (pricing, ACV, sales motion)?",
  "traction": "What proof do you have (users, revenue, pilots, LOIs, retention, metrics)?",
  "moat": "What’s defensible (data, distribution, workflow lock-in, network effects, IP)?",
  "ask": "What are you raising / asking for and how will you use it over the next 12–18 months?"
}

def next_stage(current: str) -> str:
  if current not in STAGES:
    return "one_liner"
  idx = STAGES.index(current)
  return STAGES[min(idx + 1, len(STAGES) - 1)]