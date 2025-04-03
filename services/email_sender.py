import smtplib
from email.mime.text import MIMEText

# def send_email(to, subject, body):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = "noreply@meteostation.com"
#     msg['To'] = "mectp@yandex.ru"
    
#     with smtplib.SMTP('smtp.server.com', 587) as server:
#         server.starttls()
#         server.login("user", "password")
#         server.send_message(msg)

def send_email(to_email, subject, body):
    """Отправка через MailHog для тестирования"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "test@meteostation.com"
    msg['To'] = to_email
    
    try:
        with smtplib.SMTP('localhost', 1025) as server:  # MailHog порт
            server.send_message(msg)
        print(f"Test email sent to {to_email}")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")