import logging
import os
import smtplib
import time
from email.message import EmailMessage

log = logging.getLogger("timing")


def send_email(to: str, subject: str, body: str) -> dict[str, str]:
    gmail_address = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_address or not app_password:
        log.error("email: GMAIL_ADDRESS or GMAIL_APP_PASSWORD missing")
        return {"ok": "false", "message": "Gmail is not configured."}
    if not to:
        log.error("email: recipient (EMAIL_TO) is empty")
        return {"ok": "false", "message": "No recipient."}

    message = EmailMessage()
    message["From"] = gmail_address
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    start = time.perf_counter()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.starttls()
            server.login(gmail_address, app_password)
            server.send_message(message)
        log.info("email: sent in %.0f ms", (time.perf_counter() - start) * 1000)

        return {"ok": "true", "message": "Email sent successfully."}

    except (smtplib.SMTPException, OSError) as error:
        log.exception("email: FAILED (%s)", type(error).__name__)
        return {"ok": "false", "message": f"Failed to send email: {error}"}