## Environmental AI Coach 🌱

An intelligent environmental coaching system that provides personalized environmental advice, air quality monitoring, and interactive quizzes to help users improve their environmental impact.
Features
🗺️ Location-based environmental analysis and recommendations
💨 Real-time air quality monitoring (PM2.5 and PM10)
🎯 Interactive environmental quizzes with points system
🤖 AI-powered personalized advice
🎮 Gamification elements to encourage engagement
🌐 Multiple interfaces (CLI, Web UI, API)

### Prerequisites
Python >=3.10 <=3.13
UV package manager (recommended)



## Installation

```
### Install UV if you haven't already:
```

```bash
pip install uv
```
```bash
get clone https://github.com/koookieee/AgenticAICoach
cd coach_environmental_ai
```

## Add entries to .env file


```bash
OPENAI_API_KEY=
SERPER_API_KEY=
```

## Running the application

### Option 1: Gradio Web Interface
The Gradio interface provides an intuitive web-based UI for interacting with the Environmental AI Coach.

NOTE: First make sure you are inside: src/environmental_ai_coach


```bash
python -m gradio_ui
```
This will launch a web interface at http://localhost:7860



### Option 2: API
The API provides a RESTful API for interacting with the Environmental AI Coach.
DOCS at: `http://localhost:8000/docs`
NOTE: First make sure you are inside: src/environmental_ai_coach


```bash
python -m gradio_ui
```
This will launch a web interface at http://localhost:7860

### API Endpoints:
POST /environmental-advice: Get personalized environmental advice
POST /quiz-answer: Submit quiz answers and get feedback

### Example API request:
```bash
curl -X POST "http://localhost:8000/environmental-advice" -H "Content-Type: application/json" -d '{"location": "New York", "user_input": "I want to reduce my carbon footprint", "user_points": 0}'
```

---

# Credit and Contact

Special thanks to [Vidushee Vats](https://www.linkedin.com/in/vidushee-vats/) for this valuable contribution. Connect with them on GitHub or LinkedIn for further discussion.