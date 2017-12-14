"""
**************************************************
API Functions:

get_credentials()


Google Apps for Business API Class
**************************************************
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# #testing import
# from src.login import UserManager
# from src.event import Event


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Tattoo Appointment Maker'

# #testing on this file
# USER_MANAGER = UserManager()


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def add_to_calendar(evnt):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # # testing here
    # username = 'Jplemel'
    # user = USER_MANAGER.get_user_profile(username)
    # studio = USER_MANAGER.get_studio_profile('Rad Tattoo Shop')
    # user_id = user.user_id
    # summary = user.first_name + ' ' + user.last_name + ' Tattoo Appointment'
    # location = studio.studio_name
    # tattoo = 'Tattoo: Medusa //'
    # tattoo_size = 'Size: Large //'
    # tattoo_location = 'Rad Tattoo Shop'
    # description = user.email_address + tattoo + tattoo_size + tattoo_location
    #
    # # if 12-4
    # year = '2017-'
    # month = '12-'
    # day = '11'
    # date = year+month+day

    # # Set appointment time 12-4pm
    # time_start_noon = 'T12:00:00-06:00'
    # time_end_four = 'T16:00:00-06:00'
    #
    # # 12-4pm start & end datetimes
    # start_datetime_noontofour = date + time_start_noon
    # end_datetime_noontofour = date + time_end_four
    #
    # # Set appointment time 4-8pm
    # time_start_four = 'T16:00:00-06:00'
    # time_end_eight = 'T20:00:00-06:00'
    #
    # # 4-8pm start & end datetimes
    # start_datetime_fourtoeight = date + time_start_four
    # end_datetime_fourtoeight = date + time_end_eight
    #
    # start_datetime = '2017-12-10T12:00:00-06:00'
    # end_datetime = '2017-12-10T16:00:00-06:00'
    # timezone = 'America/Chicago'
    # attendee_studio = studio.admin_email_address
    # attendee_user = 'jenniferlynn.plemel@gmail.com'
    #
    # try:
    #     USER_MANAGER.add_event(user_id, summary, location, description, start_datetime, end_datetime, timezone,
    #                            attendee_studio, attendee_user)
    # except ReferenceError:
    #     print('failed to complete appointment request')

    # evnt = Event(user_id=user_id, summary=summary, location=location, description=description,
    #              start_datetime=start_datetime_fourtoeight, end_datetime=end_datetime_fourtoeight,
    #              timezone=timezone,
    #              attendee_studio=attendee_studio, attendee_user=attendee_user)

    print('Trying to create event' + evnt.summary)
    event = {
        'summary': evnt.summary,
        'location': evnt.location,
        'description': evnt.description,
        'start': {
            'dateTime': evnt.start_datetime,
            'timeZone': evnt.timezone,
        },
        'end': {
            'dateTime': evnt.end_datetime,
            'timeZone': evnt.timezone,
        },
        'attendees': [
            {'email': evnt.attendee_user},
            {'email': evnt.attendee_studio},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



