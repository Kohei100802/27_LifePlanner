from __future__ import annotations
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.features.auth import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
        birth_year=data.birth_year,
        birth_month=data.birth_month,
        birth_day=data.birth_day,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> models.User | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
