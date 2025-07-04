# 🧠 AI Feature Clarity Coach

The **AI Feature Clarity Coach** is an intelligent chat assistant that guides users in refining their AI product ideas through a thoughtful, self-reflective, and supportive conversation. It simulates a coach that helps you uncover user pain points, define value, brainstorm AI solutions, and reflect on feasibility — one clear question at a time.

---

## 📘 Overview

This coach is built to support:
- AI entrepreneurs exploring product–market fit
- Product teams shaping new feature ideas
- Innovators clarifying use cases for AI-driven solutions

Rather than presenting a rigid form or checklist, the coach adapts dynamically. It evaluates what information has already been shared and progresses only when the **user has reached sufficient clarity** for the current phase.

---

## ✨ Key Features

- **User-Driven Flow**: No fixed question lists. Each phase proceeds only if the routing agent confirms you’ve provided enough clarity to move forward.
- **One Question at a Time**: Keeps interactions focused and digestible.
- **Phase-Based Conversation**:
  - Identify your **Core User Problem**
  - Clarify the **Core Value Proposition**
  - Brainstorm **AI Solutions**
  - **Validate & Reflect** on alignment and feasibility
- **Encourages Deep Thinking**: Questions are designed to provoke thoughtful reflection — not quick, surface-level answers.
- **Supportive Coaching Style**:
  - Avoids long-winded answers
  - Offers feedback only when asked
  - Uses a non-judgmental, encouraging tone

---
## 🧠 Architecture Overview
- **Routing Agent** (Flow Manager):
Decides whether the user is ready to progress to the next coaching phase based on phase-specific criteria and chat history.

- **Phase-Specific Agents**:
Each phase is handled by a dedicated agent with its own goals and prompts, defined via YAML (agents.yaml, tasks.yaml).
  - core_problem_agent
  - core_value_agent
  - solution_agent
  - validation_agent

- **Routing and State Management**:
Uses CrewAI’s Flow system and @listen, @start, and @router decorators to manage user state, conversation routing, and task delegation dynamically based on current phase and input.

- **YAML-Driven Configurability**:
Agent roles, prompts, and task logic are entirely YAML-configurable, making it easy to update coaching behavior without changing core logic.

- **Frontend**:
Built with Streamlit and backed by FastAPI, the UI enables real-time conversation and context-aware feedback with state persistence and animated assistant responses.
---
## 🧱 Tech Stack

| Technology      | Role                                      |
|----------------|-------------------------------------------|
| Python          | Core backend logic                       |
| Streamlit       | Chat-based frontend UI                   |
| FastAPI         | API server powering the conversation     |
| CrewAI          | Multi-agent orchestration framework      |
| Docker          | Containerization                         |
| Google Cloud    | Deployment target (e.g. Cloud Run)       |
| Pytest          | Testing framework                        |

---

## 🧑‍💼 Agents Overview

| Agent Name           | Role                                                    |
|----------------------|---------------------------------------------------------|
| `routing_agent`      | Evaluates current state and decides whether to stay or proceed |
| `core_problem_agent` | Helps uncover the target user and their challenges      |
| `core_value_agent`   | Guides prioritization of the most valuable problem to solve |
| `solution_agent`     | Facilitates creative brainstorming of AI feature ideas  |
| `validation_agent`   | Reflects on feasibility, user fit, and business alignment |

Each phase is initiated **only when the coach determines** that enough reflective insight has been collected.

---

## 📂 Folder Structure
```bash
.
├── main.py                  # FastAPI app
├── app.py                   # Streamlit UI
├── crew.py                  # CrewAI flow logic
├── Dockerfile               # Container setup
├── utils/
│   ├── llm_assistant.py     # LLM setup
│   ├── format.py            # Chat formatting helper
│   └── enable_logging.py    # Logging config
├── config/
│   ├── agents.yaml          # CrewAI agent definitions
│   └── tasks.yaml           # Task prompts per phase
├── tests/
│   ├── test_api.py          # Unit tests
│   └── test_coach.py        # Integartion tests
├── .env.example             # Example file for API key setup
├── requirements.txt         # Dependencies
└── README.md
```
---
## 🖼 GUI Screenshots

- Screenshot 1: Conversational interface in action
![Screenshot 2025-06-22 200350](https://github.com/user-attachments/assets/32f0bb7e-a343-4671-887c-36adab932c3f)

- Screenshot 2: Final AI idea summary shown after session
![Screenshot 2025-06-22 201101](https://github.com/user-attachments/assets/076c4b8e-8044-4839-b649-e849a671af20)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- OpenAI API key

### 2. Clone the Repo

```bash
git clone https://github.com/yourusername/ai-feature-clarity-coach.git
cd ai-feature-clarity-coach
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Set Your API Key

Create a .env file in the project root and add your OpenAI key (example: .env.example).

### 4. Run the FastAPI Backend

```bash
uvicorn main:app --reload
```

### 5. Run the Streamlit Chat UI

```bash
streamlit run app.py
```

### 6. Run Tests (optional)

```bash
pytest tests/
```
---

## 🐳 Docker Deployment (optional)

Build and run locally:

```bash
docker build -t clarity-coach .
docker run -p 8000:8000 clarity-coach
```

You can push the image to Google Cloud Container Registry and deploy via Cloud Run or GKE.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

