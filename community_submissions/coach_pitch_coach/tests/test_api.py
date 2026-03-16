from fastapi.testclient import TestClient

from pitch_coach import api
from pitch_coach.tools.storage import SessionState


def _fake_state(session_id: str) -> SessionState:
    return SessionState(
        session_id=session_id,
        stage="one_liner",
        context={"one_liner": None, "last_refined_pitch": None},
    )


def _noop(*_args, **_kwargs):
    return None


def _setup_mocks(monkeypatch):
    monkeypatch.setattr(api, "build_crew", lambda: {"agents": {}, "tasks_cfg": {}})
    monkeypatch.setattr(api, "run_structure", lambda *_args, **_kwargs: "coach reply")
    monkeypatch.setattr(api, "run_refine", lambda *_args, **_kwargs: "refined reply")
    monkeypatch.setattr(api, "run_qa", lambda *_args, **_kwargs: "qa reply")
    monkeypatch.setattr(api, "get_or_create_session", _fake_state)
    monkeypatch.setattr(api, "save_session", _noop)
    monkeypatch.setattr(api, "add_message", _noop)


def test_coach_mode(monkeypatch):
    _setup_mocks(monkeypatch)
    with TestClient(api.app) as client:
        res = client.post(
            "/coach",
            json={
                "mode": "coach",
                "user_message": "We help CFOs close the books faster.",
                "audience": "VC",
                "funding_stage": "pre-seed",
            },
        )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "coach"
    assert data["coach_response"] == "coach reply"
    assert data["next_question"]


def test_refine_mode(monkeypatch):
    _setup_mocks(monkeypatch)
    with TestClient(api.app) as client:
        res = client.post(
            "/coach",
            json={
                "mode": "refine",
                "user_message": "Our product uses AI to help finance teams.",
                "audience": "VC",
                "funding_stage": "seed",
            },
        )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "refine"
    assert data["coach_response"] == "refined reply"


def test_qa_mode(monkeypatch):
    _setup_mocks(monkeypatch)
    with TestClient(api.app) as client:
        res = client.post(
            "/coach",
            json={
                "mode": "qa",
                "user_message": "We automate monthly close for mid-market SaaS.",
                "industry": "FinTech",
                "audience": "VC",
                "funding_stage": "seed",
            },
        )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "qa"
    assert data["coach_response"] == "qa reply"
