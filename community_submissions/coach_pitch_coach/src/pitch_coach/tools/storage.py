import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import time

DEFAULT_DB_PATH = Path(__file__).resolve().parents[3] / "db" / "pitch_coach.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  stage TEXT NOT NULL,
  context_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  meta_json TEXT,
  FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);
"""

@dataclass
class SessionState:
  session_id: str
  stage: str
  context: Dict[str, Any]

def _now() -> int:
  return int(time.time())

def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
  db_path.parent.mkdir(parents=True, exist_ok=True)
  with sqlite3.connect(db_path) as con:
    con.executescript(SCHEMA)

def get_or_create_session(session_id: str, db_path: Path = DEFAULT_DB_PATH) -> SessionState:
  init_db(db_path)
  with sqlite3.connect(db_path) as con:
    cur = con.cursor()
    cur.execute("SELECT stage, context_json FROM sessions WHERE session_id = ?", (session_id,))
    row = cur.fetchone()
    if row:
      stage, ctx = row
      return SessionState(session_id=session_id, stage=stage, context=json.loads(ctx))

    default_ctx = {
      "one_liner": None,
      "problem": None,
      "solution": None,
      "uvp": None,
      "target_customer": None,
      "market": None,
      "business_model": None,
      "traction": None,
      "moat": None,
      "ask": None,
      "last_refined_pitch": None
    }
    now = _now()
    cur.execute(
      "INSERT INTO sessions(session_id, created_at, updated_at, stage, context_json) VALUES(?,?,?,?,?)",
      (session_id, now, now, "one_liner", json.dumps(default_ctx)),
    )
    con.commit()
    return SessionState(session_id=session_id, stage="one_liner", context=default_ctx)

def save_session(state: SessionState, db_path: Path = DEFAULT_DB_PATH) -> None:
  with sqlite3.connect(db_path) as con:
    con.execute(
      "UPDATE sessions SET updated_at = ?, stage = ?, context_json = ? WHERE session_id = ?",
      (_now(), state.stage, json.dumps(state.context), state.session_id),
    )
    con.commit()

def add_message(session_id: str, role: str, content: str, meta: Optional[Dict[str, Any]] = None,
                db_path: Path = DEFAULT_DB_PATH) -> None:
  with sqlite3.connect(db_path) as con:
    con.execute(
      "INSERT INTO messages(session_id, created_at, role, content, meta_json) VALUES(?,?,?,?,?)",
      (session_id, _now(), role, content, json.dumps(meta) if meta else None),
    )
    con.commit()

def get_recent_messages(session_id: str, limit: int = 12, db_path: Path = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
  with sqlite3.connect(db_path) as con:
    cur = con.cursor()
    cur.execute(
      "SELECT role, content, meta_json, created_at FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
      (session_id, limit),
    )
    rows = cur.fetchall()
  out = []
  for role, content, meta_json, created_at in reversed(rows):
    out.append({
      "role": role,
      "content": content,
      "meta": json.loads(meta_json) if meta_json else None,
      "created_at": created_at
    })
  return out