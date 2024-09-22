from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import Config


class Sender:
    @staticmethod
    def send_code(code, email):
        message = MIMEMultipart()
        message['Subject'] = 'Код подтверждения Sadok'
        message['From'] = Config.Email.EMAIL_ADDR
        message['To'] = email
        html = f"""\
        <html>
        <body>
            <p>Ваш код подтверждения:<br>
            <span style="font-size: 20px; font-weight: bold;">{code}</span><br>
            </p>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as conn:
                conn.login(user=Config.Email.EMAIL_ADDR, password=Config.Email.EMAIL_PASS)
                conn.send_message(message)
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")