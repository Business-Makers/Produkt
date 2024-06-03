from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtp_infos
from fastapi import HTTPException
import smtplib
import logging

username = smtp_infos.username
password = smtp_infos.password

logging.basicConfig(filename='email_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def send_email(receiver, subject):
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        try:
            server.login(username, password)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Incorrect username or password for Outlook connection.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Mailserver unavailable.")

    sender_mail = username
    receiver_mail = receiver
    subject_mail = "Login"
    body = "Tester Inhalt"

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_mail
        msg['To'] = receiver_mail
        msg['Subject'] = subject_mail
        msg.attach(MIMEText(body, 'plain'))

        logging.debug("Message Content:")
        logging.debug(f"From: {sender_mail}")
        logging.debug(f"To: {receiver_mail}")
        logging.debug(f"Subject: {subject_mail}")
        logging.debug(f"Body: {body}")

        try:
            text = msg.as_string()
            server.sendmail(sender_mail, receiver_mail, text)
            logging.debug("Converted Message:")
            logging.debug(text)

        except Exception as e:
            logging.error(f"Could not create msg: {e}")

    except Exception as e:
        raise HTTPException(status_code=1, detail="Could not create msg")


    finally:
        server.quit()
