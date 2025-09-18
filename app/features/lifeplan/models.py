from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text, ForeignKey
from app.infra.db import Base


class LifePlanWizard(Base):
    __tablename__ = "lifeplan_wizard"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, unique=True)
    step1: Mapped[str | None] = mapped_column(Text)
    step2: Mapped[str | None] = mapped_column(Text)
    step3: Mapped[str | None] = mapped_column(Text)
    step4: Mapped[str | None] = mapped_column(Text)
    step5: Mapped[str | None] = mapped_column(Text)
    step6: Mapped[str | None] = mapped_column(Text)
