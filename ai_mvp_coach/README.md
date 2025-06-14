# AI MVP Coach 🎯

An AI-powered coach that helps entrepreneurs validate their MVP ideas through structured self-reflection using CrewAI. Features a web interface and persistent database for chat history.

## Core Features

- **Guided Self-Reflection**: One question at a time approach
- **Risk Assessment**: Identify the riskiest assumptions in your MVP
- **Quick Validation**: Design experiments testable within 24 hours
- **Actionable Insights**: Get clear next steps for your MVP
- **Web Interface**: Modern chat interface with glass effects and animations
- **Persistent Storage**: SQLite database for chat history and session management
- **REST API**: Full API for integration and automation

## Quick Start

```bash
# Install dependencies
pip install -e .

# Initialize database (first time only)
python -m src.ai_mvp_coach.api.database

# Run the web application
python -m src.ai_mvp_coach.simple_coach

# Or run with CLI
python -m ai_mvp_coach.main
```

## Web Interface

Access the web interface at `http://localhost:8000`:
- Modern chat interface with gradient backgrounds
- Real-time message suggestions
- Session history and management
- Responsive design for all devices

## Database Features

- **Persistent Chat History**: All conversations are saved
- **Session Management**: Multiple concurrent coaching sessions
- **Analytics**: Track session statistics and response times
- **Export Capabilities**: Full conversation history via API

See [Database Documentation](../docs/DATABASE_IMPLEMENTATION.md) for detailed information.

## API Endpoints

- `POST /api/chat` - Send messages to the AI coach
- `GET /api/sessions` - List all coaching sessions
- `GET /api/sessions/{id}/conversation` - Get conversation history
- `GET /api/stats` - Get usage statistics
- `DELETE /api/sessions/{id}` - Delete sessions

## How It Works

The AI MVP Coach guides you through 4 key stages:

1. **Risk Assessment** - Identify your most uncertain assumptions
2. **Customer Discovery** - Understand your target market
3. **Problem Validation** - Confirm the problem is worth solving
4. **Solution Validation** - Test your proposed solution

## Project Structure

```
ai_mvp_coach/
├── src/ai_mvp_coach/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── simple_coach.py      # Core coaching logic
│   ├── crew.py              # CrewAI setup
│   ├── api/
│   │   ├── main.py          # FastAPI web server
│   │   ├── database.py      # Database models
│   │   ├── chat_service.py  # Database service layer
│   │   └── templates/       # HTML templates
│   ├── agents/              # AI agents
│   └── tasks/               # AI tasks
├── tests/
├── docs/                    # Documentation
└── README.md
```

## License

MIT License
