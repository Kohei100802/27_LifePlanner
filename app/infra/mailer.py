from __future__ import annotations
from typing import Optional
from app.shared.config import settings

try:
    import aiosmtplib
except Exception:  # pragma: no cover - optional dependency
    aiosmtplib = None  # type: ignore


async def send_email(to: str, subject: str, body: str) -> None:
    """Very simple mailer: if SMTP envs are set and aiosmtplib is available, send; otherwise print to console."""
    host = settings.smtp_host
    if not host or aiosmtplib is None:
        print(f"[MAIL STUB] To: {to}\nSubject: {subject}\n\n{body}")
        return

    from_email = settings.mail_from or "no-reply@example.com"
    message = f"From: {from_email}\nTo: {to}\nSubject: {subject}\n\n{body}"
    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port or 587,
        username=settings.smtp_user,
        password=settings.smtp_password,
        start_tls=True,
    )
