# 🧠 AI Confidence Coach

An interactive AI-powered coach that helps users identify and revise low-confidence communication patterns. Built with **FastAPI**, **Streamlit**, and **CrewAI**, this app provides actionable feedback to foster assertive, confident expression.

---

## 🚀 Features

- **Low-Confidence Marker Detection**  
  Identifies hedging, minimizing, apologizing, and passive voice patterns.

- **Actionable Suggestions**  
  Recommends stronger alternatives and revised wording.


- **Interactive Feedback Loop**  
  Users can revise and resubmit iteratively with encouraging guidance for improvement.

---

## 🛠 Tech Stack

- Python · FastAPI · Streamlit  
- Uvicorn (ASGI server)  
- CrewAI for agent orchestration  
- YAML-configurable agents (`agents.yaml`, `tasks.yaml`)

---

## 🧪 Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/DigitalProductschool/AgenticAICoach.git
cd community_submissions/confidence_crew
git checkout confidence_crew


```

 ### 2.Create a `.env` file in the root directory and add your Mistral API key:
```bash

MISTRAL_API_KEY="your_key_here"
```

 ### 3. Run with Docker Compose

```bash
docker-compose up --build
```

### 3. Or Run Manually
```bash

# Create and activate a virtual environment (optional but recommended)
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Backend
cd src
uvicorn confidence_crew.main:app --reload

# Frontend
cd frontend
streamlit run app.py
```


## ✅ Acceptance Criteria

- Detects low-confidence markers in user input
- Gives assertive, encouraging suggestions
- Supports iterative feedback flow
- Provides warm, supportive tone in all responses