import os
import json
import pytz
import datetime
from queue import Queue

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

############################################################################

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

def get_events(day, service, speech_queue: Queue):
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

    events = events_result.get('items', [])

    if not events:
        speech_queue.put('No upcoming events found.')
    else:
        speech_queue.put(f"You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.datetime.fromisoformat(start).strftime("%I:%M %p")
            speech_queue.put(f"{event['summary']} at {start_time}")

def get_date(text):
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
    service = authenticate_google()
    text_input = "next Monday"
    date = get_date(text_input)
    get_events(date, service)