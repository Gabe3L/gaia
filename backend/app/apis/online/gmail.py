import os
import smtplib
from typing import List

from backend.app.apis.online.google_authentication import authenticate_gmail
from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def get_unread_email_subjects() -> List[str]:
    service = authenticate_gmail()

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
    service = authenticate_gmail()
    
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