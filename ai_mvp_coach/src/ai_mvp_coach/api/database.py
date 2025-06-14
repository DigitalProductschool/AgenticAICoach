"""
Database configuration and models for AI MVP Coach
"""
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os
from pathlib import Path

# Database URL - SQLite for simplicity, easily upgradeable to PostgreSQL
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/coaching_sessions.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


class ChatSession(Base):
    """
    Model for coaching chat sessions
    """
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    current_phase = Column(String, default="risk_assessment", nullable=False)
    message_count = Column(Integer, default=0, nullable=False)
    status = Column(String, default="active", nullable=False)  # active, completed, paused
    
    # Session metadata
    user_id = Column(String, nullable=True)  # For future user authentication
    session_title = Column(String, nullable=True)  # Optional session name
    
    # Relationship to messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """
    Model for individual chat messages
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Message content
    user_message = Column(Text, nullable=False)
    coach_response = Column(Text, nullable=False)
    phase = Column(String, nullable=False)
    
    # Message metadata
    response_time_ms = Column(Integer, nullable=True)  # For performance tracking
    suggestions = Column(Text, nullable=True)  # JSON string of suggestions
    
    # Relationship to session
    session = relationship("ChatSession", back_populates="messages")


# Database dependency
def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)


def init_database():
    """
    Initialize database with tables
    """
    print("Initializing database...")
    create_tables()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_database()
