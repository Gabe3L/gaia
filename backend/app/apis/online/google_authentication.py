import os
import json
from typing import Any

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.readonly']

def _authenticate_google() -> Any:
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

    return creds

def authenticate_gmail() -> Any:
    return build('gmail', 'v1', credentials=_authenticate_google())

def authenticate_calendar() -> Any:
    return build('calendar', 'v3', credentials=_authenticate_google())