from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.shared.config import settings
from app.infra.db import get_db
from app.features.auth.models import User
from app.infra.mailer import send_email

router = APIRouter()

serializer = URLSafeTimedSerializer(settings.secret_key)


@router.get("/forgot", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return request.app.state.templates.TemplateResponse("forgot.html", {"request": request, "sent": False})


@router.post("/forgot", response_class=HTMLResponse)
async def forgot_password(request: Request, db: Session = Depends(get_db), email: str = Form(...)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        token = serializer.dumps({"email": user.email})
        reset_link = f"/reset?token={token}"
        await send_email(to=user.email, subject="パスワード再設定", body=f"以下のリンクから再設定してください: {reset_link}")
    return request.app.state.templates.TemplateResponse("forgot.html", {"request": request, "sent": True})


@router.get("/reset", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    return request.app.state.templates.TemplateResponse("reset.html", {"request": request, "token": token, "error": None})


@router.post("/reset")
async def reset_password(request: Request, db: Session = Depends(get_db), token: str = Form(...), password: str = Form(...)):
    if len(password) < 8:
        return request.app.state.templates.TemplateResponse("reset.html", {"request": request, "token": token, "error": "8文字以上にしてください"})
    try:
        data = serializer.loads(token, max_age=60 * 60 * 24)  # 24h
        email = data.get("email")
    except (BadSignature, SignatureExpired):
        return request.app.state.templates.TemplateResponse("reset.html", {"request": request, "token": token, "error": "トークンが不正/期限切れです"})

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return request.app.state.templates.TemplateResponse("reset.html", {"request": request, "token": token, "error": "ユーザーが見つかりません"})

    from app.features.auth.service import hash_password
    user.hashed_password = hash_password(password)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login", status_code=302)
