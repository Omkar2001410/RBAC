import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg['Subject'] = "Your OTP Code"
    msg['From'] = EMAIL_USERNAME
    msg['To'] = to_email
    msg.set_content(f"Your OTP is: {otp}\nIt will expire in 5 minutes.")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
