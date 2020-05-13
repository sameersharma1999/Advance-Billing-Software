from App.Database.db_changes import UploadRetrievePassword
import smtplib
from email.message import EmailMessage
import requests
import socket


class Mail:
    @classmethod
    def check_internet_connection(cls):
        try:
            requests.get('https://www.google.com/')
        except Exception:
            return False  # if internet is connected
        return True  # if internet not connected

    @classmethod
    def send_email(cls, otp):
        try:
            sender_email = 'thisisbradpitt1999@gmail.com'
            password = 'brad@gmail'

            receiver_email = UploadRetrievePassword.retrieve_email()
            message = EmailMessage()
            message['Subject'] = 'One time password'
            message['From'] = sender_email
            message['To'] = receiver_email
            message.set_content(f'Your OTP is: {str(otp)}')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as conn:
                conn.login(sender_email, password)  # login to sender email
                conn.send_message(message)  # email sent
                return True
        except socket.gaierror:  # not connected to internet
            return -1
        except smtplib.SMTPRecipientsRefused:  # email not working of user
            return -2
        except Exception as e:
            print(e)
            return False
