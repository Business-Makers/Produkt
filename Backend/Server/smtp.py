from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtp_infos
from fastapi import HTTPException
import smtplib
from utils import getMailText
from sqlalchemy.orm import Session
import logging

logging.basicConfig(filename='debugAll.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

usernameSMTP = smtp_infos.username_cont
passwordSMTP = smtp_infos.password_cont


def send_email(receiver, subject, db: Session):
    """
        Send an email with the specified subject to the given receiver.

        This function connects to the SMTP server using the provided credentials, generates the email content based on
        the receiver's email and subject, and sends the email. It logs the email content and handles exceptions that may
        occur during the process.

        Args:
            receiver (str): The email address of the receiver.
            subject (str): The subject of the email.
            db (Session): The database session to use for querying user information to generate the email content.

        Raises:
            HTTPException:
                - If the SMTP server is unavailable (status code 500).
                - If the username or password for the SMTP connection is incorrect (status code 401).
                - If there is an error creating or sending the email message (status code 500).
        """
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.set_debuglevel(1)
        server.starttls()
        try:
            server.login(usernameSMTP, passwordSMTP)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Incorrect username or password for Outlook connection.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Mailserver unavailable.")

    sender_mail = usernameSMTP
    receiver_mail = receiver
    subject_mail = subject
    body = getMailText(receiver, subject, db)

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_mail
        msg['To'] = receiver_mail
        msg['Subject'] = subject_mail
        msg.attach(MIMEText(body, 'plain'))

        try:
            text = msg.as_string()
            server.sendmail(sender_mail, receiver_mail, text)


        except Exception as e:
            return e

    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not create msg")


    finally:
        server.quit()
