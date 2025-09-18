from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.infra.db import get_db
from app.features.auth.models import User
from app.features.lifeplan import service as lp_service

router = APIRouter(prefix="/wizard")


def _require_user(request: Request, db: Session) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise RedirectResponse(url="/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise RedirectResponse(url="/login", status_code=302)
    return user


@router.get("/step/{step}", response_class=HTMLResponse)
async def step_page(step: int, request: Request, db: Session = Depends(get_db)):
    user = _require_user(request, db)
    steps = lp_service.load_steps(db, user.id)
    template = f"wizard/step{step}.html"
    return request.app.state.templates.TemplateResponse(template, {"request": request, "step": step, "data": steps.get(f"step{step}") or {}})


@router.post("/step/{step}")
async def step_save(step: int, request: Request, db: Session = Depends(get_db)):
    user = _require_user(request, db)
    form = dict(await request.form())
    lp_service.save_step(db, user.id, step, {k: v for k, v in form.items()})
    next_step = step + 1 if step < 6 else None
    return RedirectResponse(url=f"/wizard/step/{next_step}" if next_step else "/dashboard", status_code=302)
