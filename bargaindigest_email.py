"""
This file is used to digest dictionaries and send them as emails
"""
import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

def send_email(recipient_address, email_subject, email_text):
    try:
        # Load the saved credentials
        creds = Credentials.from_authorized_user_file('token.json')

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        
        # Create a message container
        message = MIMEMultipart()
        message['to'] = recipient_address
        message['subject'] = email_subject

        # Create a MIMEText object with HTML content
        html_content = MIMEText(email_text, 'html')

        # Attach the MIMEText object to the message container
        message.attach(html_content)

        # Encode the message container as a string
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Create the body dictionary with the raw message
        body = {'raw': raw_message}
        service.users().messages().send(userId='me', body=body).execute()
        print('Message sent successfully!')
    except Exception as e:
        print('An error occurred while sending the message:', str(e))

def generate_digest_html(digest_data):
    # Load the template file
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    
    # Render the template with the data
    output = template.render(data=digest_data)
    
    # Return html
    return output

if __name__ == "__main__":
    # This is just a test to see if the email is sent
    digest_text = generate_digest_html("")
    send_email('edensteven@protonmail.com', 'BargainDigest', digest_text)