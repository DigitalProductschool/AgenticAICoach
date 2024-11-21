# 🎯 Confidence Coach AI

An AI-powered communication coach that helps users improve their confidence and communication skills through real-time analysis and feedback.

## Features

- 📝 Real-time analysis of written and spoken communication
- 📊 Confidence scoring system
- 💡 Detailed feedback and improvement suggestions
- 🎤 Can process audio files (mp3)
- 📈 Progress tracking over time
- 💬 User-friendly chat interface

## Installation

- crewai
- crewai-tools
- streamlit
- PyYAML
- pydantic
- fastapi
- uvicorn


## Startup

1. Clone the repository:
bash

```
git clone https://github.com/yourusername/confidence-coach-ai.git
cd confidence-coach-ai
```

3. Install dependencies:
bash
```
pip install -r requirements.txt
```

5. Set up OpenAI API key in .env file:
bash
```
OPENAI_API_KEY=<your-openai-api-key>
```


Note: Run below commands from *confidence_coach_ai_DPS/src/confidence_coach_ai*


##Interaction Setup
### STEP1: First start the FastAPI backend
Run the following command in terminal:
bash
```
uvicorn backend.api:app --reload
```

### STEP2: Start the Streamlit UI
On terminal, run the following command:
bash
```
streamlit run streamlit_app.py
```

**then Finally open
Local URL provided in terminal for interaction**
(Note: You need to start both the FastAPI backend and Streamlit UI to interact with the app without any issues. First run the FastAPI backend and then run the Streamlit UI in different terminals)

### Optional:
- FastAPI backend docs:
Local URL: http://localhost:8000/docs for interaction

- Runing test score
1) Run the FASTAPI backend as told above
2) Run the following command in terminal:
bash
```
python test_api.py
```
