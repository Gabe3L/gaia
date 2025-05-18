import os
import json
import smtplib
from typing import List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_google():
    creds = None
    token_path = 'shared/admin/token.json'
    credentials_path = 'shared/admin/oauth_credentials.json'

    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            creds_data = json.load(token_file)
            creds = Credentials.from_authorized_user_info(info=creds_data, scopes=SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_unread_email_subjects() -> List[str]:
    service = authenticate_google()

    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])

    subjects = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject']).execute()
        headers = msg_data['payload']['headers']
        for header in headers:
            if header['name'] == 'Subject':
                subjects.append(header['value'])

    return subjects

def get_unread_email_senders() -> List[str]:
    service = authenticate_google()
    
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    
    print(f"Found {len(messages)} unread messages.")
    senders = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From']).execute()
        headers = msg_data['payload'].get('headers', [])
        for header in headers:
            if header['name'] == 'From':
                senders.append(header['value'])

    return senders

def mail(sender_email, sender_password, receiver_email, msg):
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender_email, sender_password)
        mail.sendmail(sender_email, receiver_email, msg)
        mail.close()
        return True
    except Exception as e:
        logger.error(e)
        return False

################################################################

def main():
    print(get_unread_email_senders())

################################################################

if __name__ == '__main__':
    main()