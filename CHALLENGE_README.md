# AI MVP Coach - Agentic AI Challenge Submission

## 🎯 Challenge Overview

This is our submission for the **Agentic AI Challenge**. We've built an intelligent AI MVP Coach that guides entrepreneurs through lean startup validation using agentic AI principles.

## 🤖 Agentic AI Features

### Core Agentic Capabilities
- **Multi-Phase Workflow**: Autonomous progression through 4 coaching phases
- **Context-Aware Responses**: AI adapts coaching based on conversation history
- **Dynamic Suggestion Generation**: Real-time contextual follow-up questions
- **Persistent State Management**: Maintains conversation context across sessions
- **Intelligent Phase Transitions**: Automatically advances users through validation stages

### AI Architecture
```
User Input → Risk Assessment → Customer Discovery → Problem Validation → Solution Validation
     ↓              ↓                    ↓                   ↓                    ↓
AI Processing → Context Analysis → Response Generation → Suggestion Creation → State Update
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sergyDwhiz/AgenticAICoach.git
   cd AgenticAICoach/ai_mvp_coach
   ```

2. **Install Dependencies**
   ```bash
   pip install -e .
   ```

3. **Environment Configuration**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key" > .env
   ```

4. **Initialize Database**
   ```bash
   python -m src.ai_mvp_coach.api.database
   ```

5. **Run Application**
   ```bash
   python -m src.ai_mvp_coach.api.main
   ```

6. **Access Application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🌐 Production Deployment

### Deploy to Render
1. Fork this repository
2. Connect to Render
3. Use these settings:
   - **Build Command**: `cd ai_mvp_coach && pip install -e .`
   - **Start Command**: `cd ai_mvp_coach && python -m src.ai_mvp_coach.api.main`
   - **Environment**: Add `OPENAI_API_KEY`

### Deploy to Railway
```bash
railway login
railway init
railway add
railway deploy
```

### Deploy to Heroku
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

## 📚 API Documentation

### Core Endpoints

#### Start Coaching Session
```bash
curl -X POST "https://your-app.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to validate my SaaS idea"}'
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "coach_response": "Great! Let's start by identifying your riskiest assumption...",
  "phase": "risk_assessment",
  "suggestions": ["What problem does your SaaS solve?", "Who is your target customer?"]
}
```

#### Continue Conversation
```bash
curl -X POST "https://your-app.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My SaaS helps small businesses manage inventory",
    "session_id": "uuid-from-previous-response"
  }'
```

#### Get All Sessions
```bash
curl "https://your-app.com/api/sessions"
```

#### Get Session History
```bash
curl "https://your-app.com/api/sessions/{session_id}/conversation"
```

#### Get Analytics
```bash
curl "https://your-app.com/api/stats"
```

## 🧪 Testing the Application

### Manual Testing Steps

1. **Start New Session**
   - Visit the web interface or use API
   - Send initial message about your startup idea
   - Verify AI coach responds with relevant questions

2. **Test Phase Progression**
   - Continue conversation through multiple messages
   - Observe how AI guides you through different phases
   - Check that suggestions are contextually relevant

3. **Verify Persistence**
   - Restart the application
   - Check that previous conversations are preserved
   - Confirm session history is accessible

### Example Test Scenario
```bash
# Test 1: Start coaching session
curl -X POST "https://your-app.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to build a fitness app"}'

# Test 2: Follow up with details
curl -X POST "https://your-app.com/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "It helps people track workouts and nutrition",
    "session_id": "session-id-from-test-1"
  }'

# Test 3: Check session was saved
curl "https://your-app.com/api/sessions"

# Test 4: Get conversation history
curl "https://your-app.com/api/sessions/{session-id}/conversation"
```

## 🏗️ Architecture

### Technology Stack
- **Framework**: FastAPI (Python)
- **AI Engine**: CrewAI + OpenAI GPT
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Modern HTML/CSS/JS with Tailwind
- **Deployment**: Docker-ready, multi-platform support

### Database Schema
```sql
-- Sessions table
CREATE TABLE chat_sessions (
    id VARCHAR PRIMARY KEY,
    created_at DATETIME,
    last_activity DATETIME,
    current_phase VARCHAR,
    message_count INTEGER,
    status VARCHAR
);

-- Messages table
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR REFERENCES chat_sessions(id),
    created_at DATETIME,
    user_message TEXT,
    coach_response TEXT,
    phase VARCHAR,
    response_time_ms INTEGER,
    suggestions TEXT
);
```

### AI Coaching Phases
1. **Risk Assessment**: Identify riskiest assumptions
2. **Customer Discovery**: Understand target market
3. **Problem Validation**: Confirm problem worth solving
4. **Solution Validation**: Test proposed solution

## 📊 Features Showcase

### 🎨 Modern Web Interface
- Glass morphism design
- Responsive layout
- Real-time chat interface
- Contextual suggestions
- Session management

### 🧠 Intelligent Coaching
- Phase-aware responses
- Dynamic question generation
- Conversation memory
- Progress tracking

### 📈 Analytics & Insights
- Session statistics
- Response time tracking
- User engagement metrics
- Conversation analytics

### 🔧 Developer Experience
- Complete API documentation
- Easy deployment options
- Comprehensive testing
- Clean, maintainable code

## 🌟 Why This Submission Stands Out

1. **Production Ready**: Full database, API, and web interface
2. **Truly Agentic**: AI autonomously guides users through validation phases
3. **Business Value**: Solves real entrepreneur pain points
4. **Technical Excellence**: Modern architecture, clean code, comprehensive docs
5. **User Experience**: Beautiful, intuitive interface with persistent conversations

## 📞 Support & Contact

- **GitHub**: [Repository Issues](https://github.com/sergyDwhiz/AgenticAICoach/issues)
- **Documentation**: See `/docs` folder for detailed technical docs
- **API Reference**: `/docs` endpoint when running

---

**Built for the Agentic AI Challenge - December 2024**
*Empowering entrepreneurs with intelligent AI coaching*
