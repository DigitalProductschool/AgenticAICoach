# AI MVP Coach - Database Implementation Guide

## Overview

The AI MVP Coach application now includes a persistent database layer using SQLAlchemy and SQLite to store chat sessions and messages. This enables chat history, session management, and analytics capabilities.

## Database Architecture

### Technology Stack
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy 2.0
- **Migration Tool**: Alembic (installed but not yet configured)
- **Database File Location**: `src/ai_mvp_coach/api/coaching_sessions.db`

### Database Schema

#### Chat Sessions Table (`chat_sessions`)
Stores high-level information about coaching sessions.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| `id` | VARCHAR | Unique session identifier (UUID) | Primary Key, Required |
| `created_at` | DATETIME | Session creation timestamp | Required, Auto-generated |
| `last_activity` | DATETIME | Last update timestamp | Required, Auto-updated |
| `current_phase` | VARCHAR | Current coaching phase | Required, Default: 'risk_assessment' |
| `message_count` | INTEGER | Total messages in session | Required, Default: 0 |
| `status` | VARCHAR | Session status | Required, Default: 'active' |
| `user_id` | VARCHAR | User identifier (future use) | Optional |
| `session_title` | VARCHAR | Optional session name | Optional |

**Valid Status Values**: `active`, `completed`, `paused`

**Valid Phase Values**: `risk_assessment`, `customer_discovery`, `problem_validation`, `solution_validation`

#### Chat Messages Table (`chat_messages`)
Stores individual chat messages within sessions.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| `id` | INTEGER | Auto-increment message ID | Primary Key, Auto-increment |
| `session_id` | VARCHAR | Links to chat_sessions.id | Foreign Key, Required, Indexed |
| `created_at` | DATETIME | Message timestamp | Required, Auto-generated |
| `user_message` | TEXT | User's input message | Required |
| `coach_response` | TEXT | AI coach's response | Required |
| `phase` | VARCHAR | Coaching phase when sent | Required |
| `response_time_ms` | INTEGER | AI response time in milliseconds | Optional |
| `suggestions` | TEXT | JSON array of follow-up suggestions | Optional |

### Database Relationships
- One-to-Many: `chat_sessions` → `chat_messages`
- Cascade Delete: Deleting a session removes all its messages

## Implementation Details

### File Structure
```
src/ai_mvp_coach/api/
├── database.py          # Database models and configuration
├── chat_service.py      # Service layer for database operations
├── main.py             # FastAPI app with database integration
└── coaching_sessions.db # SQLite database file (auto-created)
```

### Core Components

#### 1. Database Configuration (`database.py`)
- SQLAlchemy engine setup
- Database models (ChatSession, ChatMessage)
- Database initialization functions
- Session management with dependency injection

#### 2. Service Layer (`chat_service.py`)
- `ChatService` class with static methods
- CRUD operations for sessions and messages
- Business logic for chat operations
- Statistics and analytics functions

#### 3. API Integration (`main.py`)
- Database dependency injection
- Updated endpoints to use persistent storage
- Hybrid approach: DB for persistence, memory for AI state

## Data Flow

### New Chat Message Flow
```
1. User sends message via API/Web
2. FastAPI receives request
3. Get or create session in database
4. Get or create MVPCoachingSession in memory
5. Process message with AI coach
6. Save message to database via ChatService
7. Update session metadata
8. Return response to user
```

### Session Lifecycle
```
1. First message → Create new session (UUID generated)
2. Subsequent messages → Update existing session
3. Session remains "active" until explicitly changed
4. All messages persist regardless of app restarts
```

## API Endpoints

### Chat Operations
- **POST** `/api/chat` - Send message and get response
- **GET** `/api/sessions` - List all coaching sessions
- **GET** `/api/sessions/{session_id}/conversation` - Get full conversation history

### Session Management
- **DELETE** `/api/sessions/{session_id}` - Delete session and all messages
- **PUT** `/api/sessions/{session_id}/status` - Update session status

### Analytics
- **GET** `/api/stats` - Get overall statistics
  ```json
  {
    "total_sessions": 5,
    "active_sessions": 3,
    "total_messages": 47,
    "avg_messages_per_session": 9.4
  }
  ```

## Database Operations

### Initialization
```bash
# Initialize database (creates tables)
cd ai_mvp_coach
source venv/bin/activate
python -m src.ai_mvp_coach.api.database
```

### Viewing Data
```bash
# Connect to SQLite database
sqlite3 src/ai_mvp_coach/api/coaching_sessions.db

# Common queries
.tables                                    # List tables
.schema chat_sessions                      # Show table structure
SELECT * FROM chat_sessions;              # View all sessions
SELECT * FROM chat_messages ORDER BY created_at; # View all messages
```

### Database Statistics
```sql
-- Session statistics
SELECT
    status,
    COUNT(*) as count,
    AVG(message_count) as avg_messages
FROM chat_sessions
GROUP BY status;

-- Daily message volume
SELECT
    DATE(created_at) as date,
    COUNT(*) as messages
FROM chat_messages
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Average response time
SELECT
    AVG(response_time_ms) as avg_response_ms,
    MIN(response_time_ms) as min_response_ms,
    MAX(response_time_ms) as max_response_ms
FROM chat_messages
WHERE response_time_ms IS NOT NULL;
```

## Service Layer Methods

### ChatService Class Methods

#### Session Operations
```python
# Create new session
session = ChatService.create_session(db, session_id="optional", user_id="optional")

# Get existing session
session = ChatService.get_session(db, session_id)

# Get all sessions (paginated)
sessions = ChatService.get_all_sessions(db, limit=50)

# Update session phase
session = ChatService.update_session_phase(db, session_id, "customer_discovery")

# Update session status
session = ChatService.update_session_status(db, session_id, "completed")

# Delete session
success = ChatService.delete_session(db, session_id)
```

#### Message Operations
```python
# Add new message
message = ChatService.add_message(
    db=db,
    session_id=session_id,
    user_message="User input",
    coach_response="AI response",
    phase="risk_assessment",
    suggestions=["Follow-up question 1", "Follow-up question 2"],
    response_time_ms=1500
)

# Get session messages
messages = ChatService.get_session_messages(db, session_id)

# Get formatted conversation history
conversation = ChatService.get_conversation_history(db, session_id)
```

#### Analytics
```python
# Get overall statistics
stats = ChatService.get_session_stats(db)
```

## Example API Usage

### Starting a New Conversation
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to build an AI-powered fitness app"}'
```

**Response:**
```json
{
  "session_id": "a2af3e82-de26-4d9c-ad94-77f96f6f6e43",
  "coach_response": "That's an exciting idea! Can you tell me what specific aspect...",
  "phase": "risk_assessment",
  "timestamp": "2025-06-14T18:38:02.079585",
  "suggestions": [
    "What's the biggest assumption in your business model?",
    "Who would be most disappointed if your product didn't exist?",
    "What evidence do you have that this problem needs solving?"
  ]
}
```

### Continuing a Conversation
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My biggest assumption is that people want AI-powered workouts",
    "session_id": "a2af3e82-de26-4d9c-ad94-77f96f6f6e43"
  }'
```

### Getting Session History
```bash
curl http://localhost:8000/api/sessions/a2af3e82-de26-4d9c-ad94-77f96f6f6e43/conversation
```

## Configuration Options

### Database URL Configuration
```python
# Current (SQLite)
DATABASE_URL = f"sqlite:///{BASE_DIR}/coaching_sessions.db"

# Future PostgreSQL example
# DATABASE_URL = "postgresql://user:password@localhost/ai_mvp_coach"
```

### SQLAlchemy Engine Options
```python
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=False  # Set to True for SQL debugging
)
```

## Performance Considerations

### Indexing
- `session_id` is indexed in `chat_messages` table for fast lookups
- Primary keys are automatically indexed
- Consider adding indexes on `created_at` for time-based queries

### Response Time Tracking
- Every message records `response_time_ms` for performance monitoring
- Use this data to identify and optimize slow responses

### Memory Management
- Database handles persistence
- `MVPCoachingSession` objects kept in memory for AI state
- Memory usage scales with concurrent active sessions

## Backup and Migration

### Backup SQLite Database
```bash
# Create backup
cp src/ai_mvp_coach/api/coaching_sessions.db coaching_sessions_backup.db

# Or use SQLite backup command
sqlite3 src/ai_mvp_coach/api/coaching_sessions.db ".backup coaching_sessions_backup.db"
```

### Migrating to PostgreSQL
1. Install PostgreSQL adapter: `pip install psycopg2-binary`
2. Update `DATABASE_URL` in `database.py`
3. Run migrations (when Alembic is configured)
4. Export data from SQLite and import to PostgreSQL

## Troubleshooting

### Common Issues

#### Database Lock Errors
```
sqlite3.OperationalError: database is locked
```
**Solution**: Ensure proper session management with `get_db()` dependency

#### Missing Tables
```
sqlite3.OperationalError: no such table: chat_sessions
```
**Solution**: Run database initialization
```bash
python -m src.ai_mvp_coach.api.database
```

#### Import Errors
```
ModuleNotFoundError: No module named 'sqlalchemy'
```
**Solution**: Install dependencies
```bash
pip install sqlalchemy alembic
```

### Debug Mode
Enable SQL logging by setting `echo=True` in database engine configuration:
```python
engine = create_engine(DATABASE_URL, echo=True)
```

## Future Enhancements

### Planned Features
1. **User Authentication**: Link sessions to user accounts
2. **Session Titles**: Allow users to name their coaching sessions
3. **Export Functionality**: Export conversations to PDF/text
4. **Advanced Analytics**: Session duration, completion rates, phase progression
5. **Real-time Updates**: WebSocket support for live chat updates

### Database Migrations
1. Configure Alembic for schema versioning
2. Add migration scripts for schema changes
3. Implement rollback capabilities

### Scaling Considerations
1. **Connection Pooling**: For high-traffic scenarios
2. **Read Replicas**: Separate read/write operations
3. **Caching**: Redis for frequently accessed data
4. **Sharding**: Partition data by user or date ranges

## Conclusion

The database implementation provides a solid foundation for persistent chat storage, enabling rich features like conversation history, session management, and analytics. The current SQLite implementation is perfect for development and small deployments, with a clear path to PostgreSQL for production scaling.

The hybrid approach of using the database for persistence while keeping AI coaching state in memory provides both durability and performance, ensuring that users can resume conversations while maintaining fast AI response times.
