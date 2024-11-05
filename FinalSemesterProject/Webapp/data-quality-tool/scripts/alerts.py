import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body, to_email):
    """Sends an email alert with the specified subject and body."""
    from_email = "youremail@example.com"
    password = "yourpassword"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
