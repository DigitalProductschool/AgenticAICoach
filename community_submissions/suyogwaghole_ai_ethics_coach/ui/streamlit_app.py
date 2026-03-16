import os
import sys
from pathlib import Path
import re

import streamlit as st
from dotenv import load_dotenv

# -----------------------------
# PATH FIX (so "src." imports work)
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Load env early
load_dotenv(dotenv_path=ROOT / ".env")

# Reduce noisy warnings in Streamlit output
os.environ.setdefault("CREWAI_TELEMETRY_ENABLED", "false")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")
os.environ.setdefault("OPENAI_API_KEY", "")  # we are using Ollama

from src.responsible_ai_coach.crew import run_intake, run_report  # noqa: E402


# -----------------------------
# UI CONFIG
# -----------------------------
st.set_page_config(page_title="AI Ethics Coach", page_icon="🤖", layout="wide")
st.title("AI Ethics & Responsible AI Coach (CrewAI + Ollama)")

st.caption(
    "Chat-style coaching: describe your AI → answer intake → get risk register + action plan + templates."
)


# -----------------------------
# Helpers
# -----------------------------
def _is_numbered_answers(text: str) -> bool:
    """Detect if user pasted numbered answers like 1. ... 2. ..."""
    if not text:
        return False
    return bool(re.search(r"(^|\n)\s*1[\)\.\-:]\s+", text.strip()))


def _build_final_context(product_desc: str, answers: str) -> str:
    return f"""
AI Product Description:
{product_desc.strip()}

User Intake Answers:
{answers.strip()}
""".strip()


def _is_reset_command(text: str) -> bool:
    """Commands that start a brand-new case inside the same chat."""
    if not text:
        return False
    t = text.strip().lower()
    triggers = [
        "new case",
        "start new case",
        "reset case",
        "start over",
        "switch case",
        "switch domain",
        "hospital case",
        "start hospital",
        "start hr",
        "start healthcare",
    ]
    return any(t.startswith(x) or t == x for x in triggers)


def reset_case(keep_history: bool = True) -> None:
    """
    Reset ONLY the current case context so user can start a new domain/case
    in the same chat. Optionally keep chat messages.
    """
    keep_messages = st.session_state.get("messages", []) if keep_history else []

    # Clear everything
    for k in list(st.session_state.keys()):
        del st.session_state[k]

    # Restore messages if requested
    st.session_state.messages = keep_messages

    # Fresh case state
    st.session_state.stage = "await_description"
    st.session_state.product_description = ""
    st.session_state.intake_text = ""
    st.session_state.intake_answers = ""
    st.session_state.report = {}
    st.session_state.case_status = "in_progress"  # in_progress / completed

    # Add a short system note into chat (optional)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                "✅ New case started.\n\n"
                "Describe your AI product in 4–8 lines:\n"
                "- domain (HR/healthcare/finance/etc.)\n"
                "- who uses it and who is impacted\n"
                "- what decision it supports\n"
                "- what data it uses\n"
                "- where it’s deployed\n"
                "- human oversight / fallback"
            ),
        }
    )


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Controls")

    st.caption("Use this to switch from HR → Hospital in the same chat.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start New Case", use_container_width=True):
            reset_case(keep_history=True)
            st.rerun()

    with col2:
        if st.button("Clear Chat", use_container_width=True):
            reset_case(keep_history=False)
            st.rerun()

    st.divider()
    st.header("Local Model")
    st.code("ollama list\nollama run llama3.2:3b \"Say READY\"", language="bash")


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    # stages: await_description -> await_answers -> done
    st.session_state.stage = "await_description"

if "case_status" not in st.session_state:
    st.session_state.case_status = "in_progress"  # in_progress / completed

if "product_description" not in st.session_state:
    st.session_state.product_description = ""

if "intake_text" not in st.session_state:
    st.session_state.intake_text = ""

if "intake_answers" not in st.session_state:
    st.session_state.intake_answers = ""

if "report" not in st.session_state:
    st.session_state.report = {}


# Seed welcome message once
if not st.session_state.messages:
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                "Hi — I’m your Responsible AI Coach.\n\n"
                "Describe your AI product in 4–8 lines:\n"
                "- domain (HR/healthcare/finance/etc.)\n"
                "- who uses it and who is impacted\n"
                "- what decision it supports\n"
                "- what data it uses\n"
                "- where it’s deployed\n"
                "- human oversight / fallback\n\n"
                "Tip: When you finish a case, type **new case** to start another."
            ),
        }
    )


# -----------------------------
# Render chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Chat input
# -----------------------------
user_text = st.chat_input("Type your message…")

if user_text:
    # Handle reset/new-case command anytime
    if _is_reset_command(user_text):
        st.session_state.messages.append({"role": "user", "content": user_text})
        reset_case(keep_history=True)
        st.rerun()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_text})

    # If case completed, allow user to either:
    # - ask follow-ups (refinement) OR
    # - start new case
    if st.session_state.case_status == "completed" and st.session_state.stage == "done":
        # Normal follow-up; user can still type "new case" anytime.
        refinement_request = user_text.strip()

        final_context = _build_final_context(
            st.session_state.product_description,
            st.session_state.intake_answers
        )

        improved_context = f"""
{final_context}

User refinement request:
{refinement_request}

Instructions:
- Keep tone supportive and objective.
- Only change what the user asked to refine.
- If user asks to switch domain/case, instruct them to type: new case
- Output updated sections clearly with headings.
""".strip()

        with st.chat_message("assistant"):
            with st.spinner("Updating based on your request…"):
                try:
                    updated = run_report(improved_context)
                    assistant_reply = (
                        "✅ Updated version:\n\n"
                        "## Risk Register\n"
                        f"{updated.get('risk_register', 'No output.')}\n\n"
                        "## Action Plan\n"
                        f"{updated.get('action_plan', 'No output.')}\n\n"
                        "## Templates\n"
                        f"{updated.get('templates', 'No output.')}\n\n"
                        "If you want to start a completely different scenario (e.g., Hospital), type: **new case**."
                    )
                except Exception as e:
                    assistant_reply = f"Error while refining:\n`{e}`"

        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.rerun()

    # -----------------------------
    # Stage-based flow
    # -----------------------------
    if st.session_state.stage == "await_description":
        st.session_state.product_description = user_text

        with st.chat_message("assistant"):
            with st.spinner("Creating intake questions…"):
                try:
                    intake = run_intake(st.session_state.product_description)
                    st.session_state.intake_text = intake
                    st.session_state.stage = "await_answers"

                    assistant_reply = (
                        "Thanks — I’ll start with a short intake to understand context.\n\n"
                        f"{intake}\n\n"
                        "Reply with your **numbered answers (1–10)**. After that, I’ll generate:\n"
                        "- a Risk Register table\n"
                        "- a step-by-step Action Plan\n"
                        "- templates/checklists"
                    )
                except Exception as e:
                    assistant_reply = (
                        "I couldn’t generate intake questions.\n\n"
                        f"Error:\n`{e}`"
                    )

        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.rerun()

    elif st.session_state.stage == "await_answers":
        if not _is_numbered_answers(user_text):
            assistant_reply = (
                "Got it — please reply in a **numbered format** so I can use it reliably.\n\n"
                "Example:\n"
                "1. Healthcare / hospital clinical decision support\n"
                "2. Primary users are doctors...\n"
                "3. The AI predicts...\n"
            )
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            st.rerun()

        st.session_state.intake_answers = user_text
        final_context = _build_final_context(
            st.session_state.product_description,
            st.session_state.intake_answers
        )

        with st.chat_message("assistant"):
            with st.spinner("Generating your Responsible AI report…"):
                try:
                    report = run_report(final_context)
                    st.session_state.report = report
                    st.session_state.stage = "done"
                    st.session_state.case_status = "completed"

                    assistant_reply = (
                        "✅ Report generated.\n\n"
                        "## Risk Register\n"
                        f"{report.get('risk_register', 'No output.')}\n\n"
                        "## Action Plan\n"
                        f"{report.get('action_plan', 'No output.')}\n\n"
                        "## Templates\n"
                        f"{report.get('templates', 'No output.')}\n\n"
                        "You can:\n"
                        "- ask follow-up questions (same case)\n"
                        "- request refinements (e.g., “add EU AI Act mapping”)\n"
                        "- start a fresh scenario (e.g., Hospital) by typing: **new case**"
                    )
                except Exception as e:
                    assistant_reply = (
                        "Something went wrong while generating the report.\n\n"
                        f"Error:\n`{e}`"
                    )

        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.rerun()

    else:
        # stage == done but case_status might be in_progress in rare cases
        assistant_reply = (
            "This case is ready for follow-ups.\n\n"
            "If you want to start a new scenario, type: **new case**"
        )
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.rerun()
