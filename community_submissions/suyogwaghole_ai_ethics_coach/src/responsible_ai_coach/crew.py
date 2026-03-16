import os
from pathlib import Path
import yaml

from crewai import Agent, Task, Crew, Process

# -----------------------------
# PATHS
# -----------------------------
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = ROOT_DIR / "config"

# -----------------------------
# ENV SAFETY
# -----------------------------
# Try to disable CrewAI telemetry/tracing early (Streamlit runs in its own runtime)
os.environ.setdefault("CREWAI_TELEMETRY_ENABLED", "false")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")

# IMPORTANT:

os.environ.setdefault("OPENAI_API_KEY", "")  # prevents "missing" errors in some setups

# -----------------------------
# OLLAMA CONFIG
# -----------------------------
# Make sure this matches EXACTLY `ollama list`
# Example shows: llama3.2:3b, llama3.2:latest, llama3.1:latest
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# CrewAI-native LLM string (this is the key fix)
# This avoids LangChain Ollama object conversion and avoids OPENAI fallback.
CREWAI_LLM = f"ollama/{OLLAMA_MODEL}"

# -----------------------------
# HELPERS
# -----------------------------
def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _render(template: str, user_input: str) -> str:
    return (template or "").replace("{{user_input}}", user_input)

def _build(task_keys: list[str], user_input: str) -> Crew:
    agents_cfg = _load_yaml(CONFIG_DIR / "agents.yaml").get("agents", {})
    tasks_cfg = _load_yaml(CONFIG_DIR / "tasks.yaml").get("tasks", {})

    if not agents_cfg:
        raise ValueError("agents.yaml did not load any agents. Check YAML formatting.")
    if not tasks_cfg:
        raise ValueError("tasks.yaml did not load any tasks. Check YAML formatting.")

    # Build agents
    agents: dict[str, Agent] = {}
    for key, a in agents_cfg.items():
        agents[key] = Agent(
            role=a.get("role", key),
            goal=a.get("goal", ""),
            backstory=a.get("backstory", ""),
            verbose=bool(a.get("verbose", True)),
            # ✅ FIX: use CrewAI-native provider string
            llm=CREWAI_LLM
        )

    # Build tasks in given order
    tasks: list[Task] = []
    for tkey in task_keys:
        if tkey not in tasks_cfg:
            raise ValueError(f"Task '{tkey}' not found in tasks.yaml")

        t = tasks_cfg[tkey]
        agent_key = t.get("agent")

        if agent_key not in agents:
            raise ValueError(
                f"Task '{tkey}' references agent '{agent_key}', but it was not found in agents.yaml"
            )

        tasks.append(
            Task(
                description=_render(t.get("description", ""), user_input),
                expected_output=t.get("expected_output", ""),
                agent=agents[agent_key]
            )
        )

    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

# -----------------------------
# PUBLIC FUNCTIONS
# -----------------------------
def run_intake(product_description: str) -> str:
    crew = _build(["intake"], product_description)
    return str(crew.kickoff())

def run_report(final_context: str) -> dict:
    outputs = {}
    for task_name in ["risk_register", "action_plan", "templates"]:
        crew = _build([task_name], final_context)
        outputs[task_name] = str(crew.kickoff())
    return outputs
