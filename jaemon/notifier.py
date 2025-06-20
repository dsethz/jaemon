import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict

logger = logging.getLogger(__name__)


def notify(jobs: List, email_cfg: Dict[str, str]) -> None:
    """Send email summary of new jobs."""
    subject = f"{len(jobs)} New Job Posts Found"
    body_lines = ["Here are your new job postings:", ""]
    for j in jobs:
        body_lines.append(f"- {j.title} ({j.date}): {j.link}")
    body = "\n".join(body_lines)

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email_cfg['from_addr']
    msg['To'] = email_cfg['to_addr']
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(email_cfg['smtp_server'], email_cfg['smtp_port']) as server:
            server.starttls()
            server.login(email_cfg['username'], email_cfg['password'])
            server.send_message(msg)
            logger.info("Notification sent: %s jobs", len(jobs))
    except Exception:
        logger.exception("Failed to send notification email")
        raise
