import smtplib
import os

from smtplib import SMTPResponseException
from .constants import BaseConstants
from email.message import EmailMessage


class EmailHandler:
    def send_email(self, from_email, to_email, subject, message):
        msg = EmailMessage()
        msg[BaseConstants.SUBJECT] = subject
        msg[BaseConstants.FROM] = from_email
        msg[BaseConstants.TO] = to_email
        msg.add_alternative(message, subtype='html')
        try:
            s = smtplib.SMTP(BaseConstants.EMAIL_URL, BaseConstants.PORT)
            s.starttls()
            s.login(
                os.environ.get("EMAIL", ""),
                os.environ.get("EMAIL_PASSWORD", ""))
            s.send_message(msg)
        except SMTPResponseException as e:
            raise BaseException(e.smtp_code, e.smtp_error)
