from __future__ import annotations
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from app.shared.config import settings
from app.infra.db import Base, engine, get_db
from app.features.auth import models as auth_models, service as auth_service, schemas as auth_schemas
from app.features.auth import reset as reset_router
from app.features.lifeplan import router as lifeplan_router

app = FastAPI(title=settings.app_name)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates  # expose for routers

# Static (Tailwind via CDN, so keep empty for now)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    user = auth_service.authenticate(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "メールまたはパスワードが違います"})
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=302)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@app.post("/register")
async def register(request: Request,
                   db: Session = Depends(get_db),
                   email: str = Form(...), name: str = Form(...), password: str = Form(...)):
    if len(password) < 8:
        return templates.TemplateResponse("register.html", {"request": request, "error": "パスワードは8文字以上"})
    exists = db.query(auth_models.User).filter(auth_models.User.email == email).first()
    if exists:
        return templates.TemplateResponse("register.html", {"request": request, "error": "既に登録済みのメールです"})
    data = auth_schemas.UserCreate(email=email, name=name, password=password)
    user = auth_service.create_user(db, data)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login")
    user = db.query(auth_models.User).filter(auth_models.User.id == user_id).first()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


# Placeholders for required pages
@app.get("/lifeplan", response_class=HTMLResponse)
async def lifeplan(request: Request):
    return templates.TemplateResponse("lifeplan.html", {"request": request})


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})


# include password reset endpoints
app.include_router(reset_router.router)
app.include_router(lifeplan_router.router)
