import re
from typing import Dict

JARGON = [
  "synergy", "paradigm", "leveraging", "disrupt", "cutting-edge", "state-of-the-art",
  "agentic", "transformative", "revolutionary", "AI-driven", "blockchain"
]

def score_text(text: str) -> Dict[str, int]:
  t = (text or "").strip()
  if not t:
    return {"clarity": 1, "persuasion": 1, "confidence": 1}

  length = len(t)
  sentences = max(1, len(re.findall(r"[.!?]", t)) or 1)
  avg_sentence_len = length / sentences

  jargon_hits = sum(1 for w in JARGON if w.lower() in t.lower())
  numbers = len(re.findall(r"\d+(\.\d+)?", t))
  hedges = len(re.findall(r"\b(maybe|might|hopefully|we think|could)\b", t.lower()))

  clarity = 8
  if avg_sentence_len > 180: clarity -= 3
  if jargon_hits >= 2: clarity -= 2
  if length < 40: clarity -= 2
  clarity = max(1, min(10, clarity))

  persuasion = 6 + (1 if numbers >= 1 else 0) + (1 if "because" in t.lower() or "so that" in t.lower() else 0)
  if length < 60: persuasion -= 2
  persuasion = max(1, min(10, persuasion))

  confidence = 7 - (2 if hedges >= 2 else 0)
  confidence = max(1, min(10, confidence))

  return {"clarity": clarity, "persuasion": persuasion, "confidence": confidence}
