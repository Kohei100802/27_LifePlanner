from __future__ import annotations
from typing import Any, Optional
from sqlalchemy.orm import Session
from app.features.lifeplan.models import LifePlanWizard
import json


def _to_json(data: dict[str, Any] | None) -> str | None:
    if data is None:
        return None
    return json.dumps(data, ensure_ascii=False)


def _from_json(text: str | None) -> dict[str, Any] | None:
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def get_or_create(db: Session, user_id: int) -> LifePlanWizard:
    row = db.query(LifePlanWizard).filter(LifePlanWizard.user_id == user_id).first()
    if row:
        return row
    row = LifePlanWizard(user_id=user_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def save_step(db: Session, user_id: int, step: int, data: dict[str, Any]) -> LifePlanWizard:
    row = get_or_create(db, user_id)
    key = f"step{step}"
    setattr(row, key, _to_json(data))
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def load_steps(db: Session, user_id: int) -> dict[str, Any]:
    row = get_or_create(db, user_id)
    return {k: _from_json(getattr(row, k)) for k in ["step1","step2","step3","step4","step5","step6"]}
