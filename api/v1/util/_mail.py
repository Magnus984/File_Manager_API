#!/usr/bin/env python3
"""Module for mail
"""
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_verification_email(to_email, verification_url):
    """Sends verification email
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    msg = MIMEText(f"Click the link to verify your email: {verification_url}")
    msg["Subject"] = "Verify Your Email"
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())