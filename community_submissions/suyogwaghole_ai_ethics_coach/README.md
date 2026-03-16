AI Ethics & Responsible AI Coach
Agentic AI System for Ethical, Transparent & Compliant AI Development








🚀 Overview

AI Ethics & Responsible AI Coach is an agent-powered system designed to help AI builders, startups, and enterprises design ethical, compliant, and trustworthy AI systems.

It acts as a virtual Responsible-AI consultant that:

Collects structured product information

Evaluates risks

Generates compliance-ready outputs

Produces governance artifacts used by auditors and regulators

This system is especially useful for:

AI startups

Healthcare & HR systems

Compliance teams

AI governance & risk professionals

🎯 What This System Does

The coach guides users through an AI ethics workflow:

Product Intake

Risk Assessment

Bias & Fairness Evaluation

Privacy & Compliance Checks

Human Oversight Validation

Governance Documentation

It outputs:

Risk Register

Action Plan

AI Governance Templates

Compliance Checklists

Audit-ready documentation

🧠 How It Works

This project uses Agentic AI (CrewAI) to coordinate specialized agents:

Agent	Role
Intake Coach	Collects product context
Risk Analyst	Identifies ethical & legal risks
Compliance Agent	Maps to GDPR, EU AI Act, HIPAA, etc
Governance Agent	Creates templates & policies

These agents collaborate to generate a full Responsible AI assessment.

🧩 Architecture
User → Streamlit Chat UI
          ↓
   FastAPI Backend
          ↓
    CrewAI Agent System
          ↓
   Risk Register + Action Plan + Templates

🌐 Live Production API

Your deployed API is live:

https://ai-ethics-coach.onrender.com


Health check:

https://ai-ethics-coach.onrender.com/


Swagger:

https://ai-ethics-coach.onrender.com/docs

📌 Example Use Cases
HR Hiring AI

Detects bias, fairness, explainability, and discrimination risks.

Healthcare AI

Evaluates patient safety, medical liability, and regulatory compliance.

Finance AI

Checks fairness, explainability, and automated decision risks.

🖥 Local Setup
1. Clone Repository
git clone https://github.com/suyogwaghole7/ai-ethics-coach.git
cd ai-ethics-coach

2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate   # Mac/Linux

3. Install Dependencies
pip install -r requirements.txt

🧪 Run Locally
Start FastAPI
uvicorn api.app:app --reload --port 8000


Open:

http://127.0.0.1:8000

http://127.0.0.1:8000/docs

💬 Streamlit Chat UI
streamlit run ui/streamlit_app.py


Chat-style Responsible AI coaching:

Enter your AI product

Answer intake questions

Receive governance documents

🔌 API Endpoints
Endpoint	Purpose
GET /	Health check
POST /intake	Generate intake questions
POST /report	Generate risk register + action plan
📦 Example API Call
POST /intake
{
  "product_description": "We are building an AI system that predicts patient risk scores from hospital records. Doctors use it to prioritize treatment."
}

☁️ Deployment (Render)

This project is deployed on Render using:

Build Command:

pip install -r requirements.txt


Start Command:

uvicorn api.app:app --host 0.0.0.0 --port 10000

🔐 Compliance Coverage

This system supports:

GDPR

EU AI Act

HIPAA

Fairness & Bias Audits

Model Governance

Human-in-the-Loop

Transparency & Explainability

🏆 Why This Matters

This project demonstrates:

Agentic AI design

AI Governance tooling

Regulatory-aware AI

Production-ready FastAPI

Ethical AI architecture

It is suitable for:

Startup incubators

AI compliance challenges

Research & enterprise demos

📄 License

MIT License