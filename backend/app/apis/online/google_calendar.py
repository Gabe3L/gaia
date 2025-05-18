import os
import json
import pytz
import datetime
from queue import Queue
from typing import List

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'

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

    return build('calendar', 'v3', credentials=creds)

def get_events(day, service) -> List[str]:
    authenticate_google()

    est = pytz.timezone('America/Toronto')

    start_of_day = datetime.datetime.combine(day, datetime.time.min).astimezone(est)
    end_of_day = datetime.datetime.combine(day, datetime.time.max).astimezone(est)
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])

def get_first_day_of_current_month() -> str:
    today = datetime.date.today()
    
    first_day = today.replace(day=1)
    
    return first_day.strftime("%A")

def get_date() -> str:
    return datetime.date.today().strftime("%m/%d/%Y")

def get_todays_events(day, service):
    authenticate_google()

    est = pytz.timezone('America/Toronto')

    start_of_day = datetime.datetime.combine(day, datetime.time.min).astimezone(est)
    end_of_day = datetime.datetime.combine(day, datetime.time.max).astimezone(est)
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])

def get_date_from_text(text):
    today = datetime.date.today()
    month = day = year = -1
    day_of_week = None

    for word in text.split():
        word_lower = word.lower()
        if word_lower in MONTHS:
            month = MONTHS.index(word_lower) + 1
        elif word_lower in DAYS:
            day_of_week = DAYS.index(word_lower)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                if ext in word:
                    try:
                        day = int(word.split(ext)[0])
                    except ValueError:
                        pass

    if month != -1 and month < today.month:
        year += 1

    if day_of_week is not None:
        today_day_of_week = today.weekday()
        diff = (day_of_week - today_day_of_week) % 7
        if "next" in text.lower():
            diff += 7
        return today + datetime.timedelta(days=diff)

    if day != -1:
        if month == -1:
            month = today.month
        if day < today.day and month == today.month:
            month += 1
        if month > 12:
            month = 1
            year += 1
        return datetime.date(year if year != -1 else today.year, month, day)

    return today

############################################################################

if __name__ == "__main__":
    speech_queue = Queue()
    text_input = "next Monday"
    date = get_date_from_text(text_input)
    events = get_events(date)
    
    if not events:
        speech_queue.put('No upcoming events found.')
    else:
        speech_queue.put(f"You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.datetime.fromisoformat(start).strftime("%I:%M %p")
            speech_queue.put(f"{event['summary']} at {start_time}")