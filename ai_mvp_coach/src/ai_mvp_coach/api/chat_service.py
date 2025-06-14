"""
Database service layer for chat operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import uuid

from .database import ChatSession, ChatMessage


class ChatService:
    """
    Service class for chat-related database operations
    """
    
    @staticmethod
    def create_session(db: Session, session_id: Optional[str] = None, user_id: Optional[str] = None) -> ChatSession:
        """
        Create a new chat session
        """
        if not session_id:
            session_id = str(uuid.uuid4())
            
        db_session = ChatSession(
            id=session_id,
            user_id=user_id,
            current_phase="risk_assessment",
            message_count=0,
            status="active"
        )
        
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[ChatSession]:
        """
        Get a chat session by ID
        """
        return db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    @staticmethod
    def get_all_sessions(db: Session, limit: int = 50) -> List[ChatSession]:
        """
        Get all chat sessions ordered by last activity
        """
        return (
            db.query(ChatSession)
            .order_by(desc(ChatSession.last_activity))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def update_session_phase(db: Session, session_id: str, phase: str) -> Optional[ChatSession]:
        """
        Update the current phase of a session
        """
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.current_phase = phase
            session.last_activity = datetime.utcnow()
            db.commit()
            db.refresh(session)
        return session
    
    @staticmethod
    def add_message(
        db: Session, 
        session_id: str, 
        user_message: str, 
        coach_response: str, 
        phase: str,
        suggestions: Optional[List[str]] = None,
        response_time_ms: Optional[int] = None
    ) -> ChatMessage:
        """
        Add a new message to a chat session
        """
        # Convert suggestions to JSON string
        suggestions_json = json.dumps(suggestions) if suggestions else None
        
        db_message = ChatMessage(
            session_id=session_id,
            user_message=user_message,
            coach_response=coach_response,
            phase=phase,
            suggestions=suggestions_json,
            response_time_ms=response_time_ms
        )
        
        db.add(db_message)
        
        # Update session message count and last activity
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.message_count += 1
            session.last_activity = datetime.utcnow()
            session.current_phase = phase
        
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def get_session_messages(db: Session, session_id: str) -> List[ChatMessage]:
        """
        Get all messages for a session
        """
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at)
            .all()
        )
    
    @staticmethod
    def get_conversation_history(db: Session, session_id: str) -> Dict[str, Any]:
        """
        Get formatted conversation history for a session
        """
        session = ChatService.get_session(db, session_id)
        if not session:
            return None
            
        messages = ChatService.get_session_messages(db, session_id)
        
        conversation = []
        for message in messages:
            suggestions = json.loads(message.suggestions) if message.suggestions else []
            conversation.append({
                "timestamp": message.created_at,
                "user_message": message.user_message,
                "coach_response": message.coach_response,
                "phase": message.phase,
                "suggestions": suggestions,
                "response_time_ms": message.response_time_ms
            })
        
        return {
            "session_id": session.id,
            "conversation": conversation,
            "session_info": {
                "created_at": session.created_at,
                "last_activity": session.last_activity,
                "message_count": session.message_count,
                "current_phase": session.current_phase,
                "status": session.status,
                "session_title": session.session_title
            }
        }
    
    @staticmethod
    def delete_session(db: Session, session_id: str) -> bool:
        """
        Delete a chat session and all its messages
        """
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
            return True
        return False
    
    @staticmethod
    def update_session_status(db: Session, session_id: str, status: str) -> Optional[ChatSession]:
        """
        Update session status (active, completed, paused)
        """
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.status = status
            session.last_activity = datetime.utcnow()
            db.commit()
            db.refresh(session)
        return session
    
    @staticmethod
    def get_session_stats(db: Session) -> Dict[str, Any]:
        """
        Get overall statistics about chat sessions
        """
        total_sessions = db.query(ChatSession).count()
        active_sessions = db.query(ChatSession).filter(ChatSession.status == "active").count()
        total_messages = db.query(ChatMessage).count()
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "total_messages": total_messages,
            "avg_messages_per_session": total_messages / total_sessions if total_sessions > 0 else 0
        }
