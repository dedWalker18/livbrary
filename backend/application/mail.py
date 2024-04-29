from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import *
import os

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "no_reply@livbrary.com"
SENDER_PASSWORD = ""


def send_email(to, subject, msg, attachment=None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["Subject"] = subject
    mail["To"] = to

    mail.attach(MIMEText(msg, "html"))

    if attachment is not None:
        with open(attachment, "rb") as attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename={attachment[len('static/downloads/'):]}")
        mail.attach(part)

    s = SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.send_message(mail)
    s.quit()
    # if attachment is not None:
    #     os.remove(attachment)

    return True