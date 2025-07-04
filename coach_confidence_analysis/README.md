# 🎯 Coach Confidence

An AI-powered coaching tool designed to help users improve their confidence through personalized feedback, analysis, and actionable recommendations.

## 📋 Overview

Coach Confidence is part of the AgenticAICoach ecosystem, using the CrewAI framework to create an intelligent coaching experience that analyzes communication patterns, identifies areas of low confidence, and provides constructive suggestions for improvement.

## ✨ Key Features

- **Confidence Analysis**: Analyzes user text and identifies language patterns that may indicate low confidence
- **Personalized Feedback**: Provides tailored suggestions to improve confidence in communication
- **Action Planning**: Helps users develop specific strategies to build confidence over time
- **Progress Tracking**: Monitors improvement and adjusts recommendations accordingly
- **User-Friendly Interface**: Simple API-based interaction for seamless integration

## 🛠️ Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Framework**: [CrewAI](https://github.com/crewAI/crewAI)
- **Language Model Integration**: Gemini
- **Server**: [Uvicorn](https://www.uvicorn.org/)


## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AgenticAICoach.git
cd AgenticAICoach/coach_confidence_analysis
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env to add your API keys
```

## 💻 Usage

1. Start the FastAPI server:
```bash
poetry run uvicorn src.coach_confidence.main:app --reload
```

2. Start Gradio App
```bash
python app.py
```


3. Use the API endpoints to interact with the confidence coach.
```bash
http://127.0.0.1:8000/analyze
```
