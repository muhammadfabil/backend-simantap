from app.core.logging import logger
from email.mime.text import MIMEText
from app.core.config import settings

import smtplib


def send_reset_password_email(to_email: str, reset_link: str):
    reset_link = f"{settings.frontend_url}/reset-password?token={reset_link}"
    
    subject = "Reset Password"
    body = f"Click the link below to reset your password:\n\n{reset_link}\n\nIf you didn’t request this, ignore this email."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.smtp_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            logger.info(f"Sending email to {to_email}")
            server.sendmail(settings.smtp_user, to_email, msg.as_string())
            logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.info(f"Error sending email: {e}")
        raise