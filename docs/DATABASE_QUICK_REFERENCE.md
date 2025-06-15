# Database Quick Reference Guide

## Quick Start Commands

### Database Setup
```bash
# Install dependencies
cd ai_mvp_coach
source venv/bin/activate
pip install sqlalchemy alembic

# Initialize database
python -m src.ai_mvp_coach.api.database
```

### Run Application
```bash
# Start the FastAPI server
python -m src.ai_mvp_coach.simple_coach
# or
uvicorn src.ai_mvp_coach.api.main:app --reload
```

## Common Database Operations

### View Database Contents
```bash
# Connect to database
sqlite3 src/ai_mvp_coach/api/coaching_sessions.db

# Quick queries
.tables                                # List all tables
SELECT COUNT(*) FROM chat_sessions;   # Count sessions
SELECT COUNT(*) FROM chat_messages;   # Count messages
SELECT * FROM chat_sessions ORDER BY last_activity DESC LIMIT 5; # Recent sessions
```

### API Testing
```bash
# Get all sessions
curl http://localhost:8000/api/sessions

# Get statistics
curl http://localhost:8000/api/stats

# Start new conversation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to validate my startup idea"}'

# Continue conversation (use session_id from previous response)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My idea is a meal planning app", "session_id": "YOUR_SESSION_ID"}'
```

## Database Schema Quick Reference

### chat_sessions
- `id` (VARCHAR, PK) - Session UUID
- `created_at` (DATETIME) - Creation time
- `last_activity` (DATETIME) - Last update
- `current_phase` (VARCHAR) - Coaching phase
- `message_count` (INTEGER) - Number of messages
- `status` (VARCHAR) - active/completed/paused

### chat_messages
- `id` (INTEGER, PK) - Auto-increment ID
- `session_id` (VARCHAR, FK) - Links to session
- `created_at` (DATETIME) - Message time
- `user_message` (TEXT) - User input
- `coach_response` (TEXT) - AI response
- `phase` (VARCHAR) - Coaching phase
- `response_time_ms` (INTEGER) - Response time
- `suggestions` (TEXT) - JSON suggestions array

## Useful SQL Queries

```sql
-- Sessions by status
SELECT status, COUNT(*) FROM chat_sessions GROUP BY status;

-- Average messages per session
SELECT AVG(message_count) FROM chat_sessions;

-- Messages per day
SELECT DATE(created_at) as date, COUNT(*) as count 
FROM chat_messages 
GROUP BY DATE(created_at) 
ORDER BY date DESC;

-- Average response time
SELECT AVG(response_time_ms) as avg_ms FROM chat_messages;

-- Most recent conversations
SELECT s.id, s.created_at, s.message_count, 
       m.user_message, m.coach_response
FROM chat_sessions s
JOIN chat_messages m ON s.id = m.session_id
WHERE m.id = (
    SELECT MAX(id) FROM chat_messages WHERE session_id = s.id
)
ORDER BY s.last_activity DESC;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `database is locked` | Check that database sessions are properly closed |
| `no such table` | Run `python -m src.ai_mvp_coach.api.database` |
| `Import errors` | Install dependencies: `pip install sqlalchemy alembic` |
| `Connection refused` | Make sure FastAPI server is running on port 8000 |

## File Locations
- Database: `src/ai_mvp_coach/api/coaching_sessions.db`
- Models: `src/ai_mvp_coach/api/database.py`
- Service: `src/ai_mvp_coach/api/chat_service.py`
- API: `src/ai_mvp_coach/api/main.py`
