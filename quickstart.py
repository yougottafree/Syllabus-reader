from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    add_event("Trial", "2020-12-24", service)

def add_event(title, date, service,  location = "", description = ""):
    """
    This function will add the event to the google calendar
    @param:
        title: the string represent title of the event
        location: the string represnt location of the event
        description: the description of the project
        date: yyyy-mm-dd
        service: the google calendar instance that we are pushing the 
                event to
    @return : void
    """
    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    event = {
    'summary': title,
    'location': location,  
    'description': description,
    'start': {
        'date': date,
        'timeZone': 'America/Phoenix',
    },
    'end': {
        'date': date,
        'timeZone': 'America/Phoenix',
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'popup', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        {'method': 'popup', 'minutes': 24*60*2},
        {'method': 'popup', 'minutes': 24*60*3},
        {'method': 'popup', 'minutes': 24*60*7}
        ],
    },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':
    main()