from src.database import Database
from src.user import User
from src.event import Event
from src.booked import Booked
import src.api
import bcrypt


""" Manage User Login"""


class UserManager:

    def __init__(self):
        self.database = Database()

    def add_user(self, first_name, last_name, username, email_address, password):
        """ Add User to DB """

        if self.find_user(username, email_address) is None:
            user = User(first_name=first_name, last_name=last_name, user_name=username, email_address=email_address,
                        password=password)
            self.database.add_user(user)
        else:
            raise RuntimeError('User already exists')

    def add_event(self, user_id, summary, location, description, start_datetime, end_datetime, timezone, attendee_studio,
                  attendee_user):
        """ Add Event to DB """
        if self.find_event(description) is None:
            event = Event(user_id=user_id, summary=summary, location=location, description=description, start_datetime=start_datetime,
                          end_datetime=end_datetime, timezone=timezone, attendee_studio=attendee_studio,
                          attendee_user=attendee_user)
            self.database.add_event(event)
        print('Event added to DB @ Start time: ' + event.start_datetime)

    def add_booked(self, event, studio_id):
        """ Add event that has been scheduled to Booked table DB"""
        # if it doesn't already exist...
        if self.find_booked_by_id(event.user_id, event.event_id, event.description) is None:
            booked = Booked(studio_id=studio_id, event_id=event.event_id, user_id=event.user_id, summary=event.summary,
                            location=event.location, description=event.description, start_datetime=event.start_datetime,
                            end_datetime=event.end_datetime, timezone=event.timezone,
                            attendee_studio=event.attendee_studio, attendee_user=event.attendee_user)
            self.database.add_booked_event(booked)

    def get_user_profile(self, username):
        """ Query DB + return user by user_name """
        user = self.database.get_user(username)
        return user

    def get_studio_profile(self, studio_name):
        """ Query DB + return user by user_name """
        studio = self.database.get_studio(studio_name)
        return studio

    def find_user(self, username, email):
        """ Query DB for user_name or email_address"""
        user = self.database.get_user(username)
        if user is not None:
            return user
        return self.database.find_user_with_email(email)

    def find_event(self, description):
        """ Query DB for Event """
        event = self.database.find_event(description)
        if event is not None:
            return event

    def find_booked_by_id(self, uid, eid, desc):
        """ Query DB for booked by booked_id """
        booked = self.database.find_booked(uid, eid, desc)
        if booked is not None:
            return booked

    def event_list(self):
        """ Query DB for all Events"""
        all_events = self.database.event_list()
        return all_events

    def booked_list(self):
        """ Query DB for all Booked Events """
        all_booked_events = self.database.booked_list()
        return all_booked_events

    def event_list_by_id(self, uid):
        """ Query DB for all Events w/user id: uid """
        all_events = self.database.event_list_by_userid(uid)
        return all_events

    def delete_event(self, eid):
        """ Query DB for event with event_id == eid and remove from DB"""

        self.database.delete_event_by_event_id(eid)

    def validate_credentials(self, username, password):
        """ Validate password matches DB password """
        user = self.database.get_user(username)

        if user is None:
            return False

        # does the password match the DB password
        if password == user.password:
            return True

    def check_if_admin(self, usermame, password, studio_name):
        """ Check if the user logging in is an admin account"""
        user = self.database.get_user(usermame)
        shopadmin = self.database.get_studio(studio_name)
        if user is None:
            return False
        if password == user.password:
            if studio_name == shopadmin.studio_name:
                if user.email_address == shopadmin.admin_email_address:
                    return True

    def add_to_calendar(self, event):
        """ Add Event to Google Calendar """
        # Sends event data to add to calendar, returns html link to cal event
        src.api.add_to_calendar(event)




