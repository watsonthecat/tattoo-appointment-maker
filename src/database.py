from sqlalchemy import exc, Table, MetaData, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from src.user import User
from src.studios import Studio
from config import Keys
from src.event import Event
from src.booked import Booked

# conn_str = will resolve a connection string from environment variable
# this value will be overwritten if the caller sends their own conn_str in the constructor
conn_str = environ.get('DATABASE_URL', 'sqlite:///data_store.db')


class Database:
    """ Data Access Layer """
    def __init__(self, connection_string='sqlite:///data_store.db'):
        self.sql_file = connection_string
        self.engine = self._get_connection()
        self.metadata = MetaData(bind=self.engine)

    def _get_connection(self):
        engine = create_engine(self.sql_file)
        return engine

    def _get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def add_user(self, user):
        """ Add a new user to the database """
        session = self._get_session()
        session.add(user)
        session.commit()

    def get_user(self, username):
        """ Get a user by username """
        session = self._get_session()

        for user in session.query(User).filter_by(user_name=username):
            return user

    def event_list(self):
        session = self._get_session()

        event_list = session.query(Event).all()
        return event_list

    def booked_list(self):
        session = self._get_session()

        booked_list = session.query(Booked).all()
        return booked_list

    def event_list_by_userid(self, uid):
        """ Get a list of requests (events) by user id"""
        session = self._get_session()

        event_list = session.query(Event).filter_by(user_id=uid).all()

        return event_list

    def delete_event_by_event_id(self, eid):
        """ Delete event from DB with event id == eid """
        session = self._get_session()

        event_to_del = session.query(Event).filter_by(event_id=eid).one()

        session.delete(event_to_del)
        session.commit()
        print('Deleted event from DB')

    def find_user_with_email(self, email):
        """ Get a user by email"""
        session = self._get_session()
        for user in session.query(User).\
            filter(User.email_address == email):
            return user

    def check_studio(self, string):
        """ Checks to see if Tattoo Studio exists in DB """
        search_session = self._get_session()
        count = search_session.query(Studio).filter_by(studio_name=string).count()

        if count > 0:
            search_session.close()
            return True
        else:
            search_session.close()
            return False

    def check_user(self, string):
        """ Checks to see if User exists in DB """
        search_session = self._get_session()
        count = search_session.query(User).filter_by(user_name=string).count()

        if count > 0:
            search_session.close()
            return True
        else:
            search_session.close()
            return False

    def get_studio(self, studio_name):
        """ Get a studio by studio_name """
        search_session = self._get_session()

        for studio in search_session.query(Studio).filter_by(studio_name=studio_name):
            return studio

    def find_event(self, description):
        """ Get a event by description """
        session = self._get_session()

        for event in session.query(Event).filter_by(description=description):
            return event

    def find_booked(self, uid, eid, desc):
        """ Get a booked event by user id and event id"""
        session = self._get_session()

        for booked in session.query(Booked).filter_by(user_id=uid, event_id=eid, description=desc):
            return booked

    def add_event(self, event):
        """ Add a new event to the database """
        session = self._get_session()
        session.add(event)
        session.commit()

    def add_booked_event(self, booked):
        """ Add an event that has been booked to the database"""

        session = self._get_session()
        session.add(booked)
        session.commit()

    def populate_generic_data(self):
        """
        Populate Studio Table with a Generic Tattoo Shop
        Note: this would be replaced with customer data/people who buy this software

        """
        save_session = self._get_session()
        # Create Studio object; use named args to set values of the object
        test_studio = Studio(studio_name='Rad Tattoo Shop', admin_email_address=Keys.personal_email,
                            studio_url='www.blackendtattoo.com/')

        # if it doesn't already exist
        if not (self.check_studio(test_studio.studio_name)):
            # Add testStudio object to session
            # This maps the object to a row in the DB
            save_session.add(test_studio)
            print('Added ' + test_studio.studio_name + ' to DB')

        # Doesn't save to DB until session is committed, or closed

        save_session.commit()

        # Checking to make sure it was added, and ID auto generated like it's supposed to
        studio = self.get_studio('Rad Tattoo Shop')
        print(studio)

    def populate_generic_user(self):

        """ Populates DB with Tattoo admin account

        Note: This would be replaced with customer data/people who buy this software

        """
        other_session = self._get_session()

        test_user = User(first_name='Jen', last_name='P', user_name='Jplemel', email_address=Keys.personal_email,
                         password="asdf")
        # if it doesn't already exist
        print(test_user.user_name)
        if not (self.check_user(test_user.user_name)):
            # Add testStudio object to session
            # This maps the object to a row in the DB
            other_session.add(test_user)
            print('Added ' + test_user.user_name + ' to DB')

        # Commit to save changes
        other_session.commit()
        new_guy = self.get_user('bs')
        print(new_guy)

    # I don't think I need this, because my User Class inherits Base (attached/mapped to engine)
    # It should automatically create a table w/set metadata(parameters)
    # def _create_tables(self):
    #     users = Table('Users', self.metadata,
    #         Column('user_id', Integer, primary_key=True),
    #         Column('first_name', String),
    #         Column('last_name', String),
    #         Column('user_name', String),
    #         Column('password', String),
    #         Column('email_address', String))
    #     users.create(self.engine, checkfirst=True)

    #    return users


if __name__ == '__main__':
    _ = Database()
