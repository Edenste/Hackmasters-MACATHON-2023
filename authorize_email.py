"""
You need to run this first in order to setup an email from which to send the emails from
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Load credentials from the JSON file
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
creds = flow.run_local_server(port=0)

# Save the credentials for later use
with open('token.json', 'w') as token_file:
    token_file.write(creds.to_json())