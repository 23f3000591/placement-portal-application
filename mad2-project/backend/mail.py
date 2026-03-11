import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "admin@placementportal.com"

def send_email(to_email, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)

        print("Email sent to", to_email)

    except Exception as e:
        print("Email failed:", e)