import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import yaml
from pathlib import Path

load_dotenv()

BASE = Path(__file__).resolve().parent
CFG = BASE / "config"

def _load_yaml(p: Path):
  with open(p, "r", encoding="utf-8") as f:
    return yaml.safe_load(f)

def build_crew():
  agents_cfg = _load_yaml(CFG / "agents.yaml")
  tasks_cfg = _load_yaml(CFG / "tasks.yaml")

  if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set")

  pitch_strategist = Agent(**agents_cfg["pitch_strategist"])
  messaging_coach = Agent(**agents_cfg["messaging_coach"])
  investor_simulator = Agent(**agents_cfg["investor_simulator"])
  progress_tracker = Agent(**agents_cfg["progress_tracker"])

  return {
    "agents": {
      "pitch_strategist": pitch_strategist,
      "messaging_coach": messaging_coach,
      "investor_simulator": investor_simulator,
      "progress_tracker": progress_tracker
    },
    "tasks_cfg": tasks_cfg
  }

def run_structure(crew_parts, stage: str, context: dict, user_message: str, audience: str, funding_stage: str):
  tcfg = crew_parts["tasks_cfg"]["structure_pitch"]
  agent = crew_parts["agents"]["pitch_strategist"]

  task = Task(
    description=tcfg["description"].format(
      stage=stage,
      context=context,
      user_message=user_message,
      audience=audience,
      funding_stage=funding_stage,
    ),
    expected_output=tcfg["expected_output"],
    agent=agent,
  )
  crew = Crew(agents=[agent], tasks=[task], verbose=True)
  return crew.kickoff()

def run_refine(crew_parts, pitch_text: str, audience: str, funding_stage: str):
  tcfg = crew_parts["tasks_cfg"]["refine_messaging"]
  agent = crew_parts["agents"]["messaging_coach"]

  task = Task(
    description=tcfg["description"].format(
      pitch_text=pitch_text,
      audience=audience,
      funding_stage=funding_stage,
    ),
    expected_output=tcfg["expected_output"],
    agent=agent,
  )
  crew = Crew(agents=[agent], tasks=[task], verbose=True)
  return crew.kickoff()

def run_qa(crew_parts, industry: str, funding_stage: str, pitch_summary: str, audience: str):
  tcfg = crew_parts["tasks_cfg"]["simulate_investor_qa"]
  agent = crew_parts["agents"]["investor_simulator"]

  task = Task(
    description=tcfg["description"].format(
      industry=industry,
      funding_stage=funding_stage,
      pitch_summary=pitch_summary,
      audience=audience,
    ),
    expected_output=tcfg["expected_output"],
    agent=agent,
  )
  crew = Crew(agents=[agent], tasks=[task], verbose=True)
  return crew.kickoff()