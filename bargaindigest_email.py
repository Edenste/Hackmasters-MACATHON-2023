"""
This file is used to digest dictionaries and send them as emails
"""
import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText

def send_email(recipent_address, email_subject, email_text):
    try:
        # Load the saved credentials
        creds = Credentials.from_authorized_user_file('token.json')

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        
        # Create a message
        message = MIMEText(email_text)
        message['to'] = recipent_address
        message['subject'] = email_subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        body = {'raw': raw_message}
        service.users().messages().send(userId='me', body=body).execute()
        print('Message sent successfully!')
        return message
    except Exception as e:
        print('An error occurred while sending the message:', str(e))



if __name__ == "__main__":
    # This is just a test to see if the email is sent
    send_email('edensteven@protonmail.com', 'Test', 'This is a test email')