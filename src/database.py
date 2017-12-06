from sqlalchemy import exc, Table, MetaData, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from src.user import User
from src.studios import Studio

# conn_str = will resolve a connection string from environment variable
# this value will be overwritten if the caller sends their own conn_str in the constructor
conn_str = environ.get('DATABASE_URL', 'sqlite:///data_store.db')


class Database:
    """ Data Access Layer """
    def __init__(self, connection_string='sqlite:///data_store.db'):
        self.sql_file = connection_string
        self.engine = self._get_connection()
        self.metadata = MetaData(bind=self.engine)

        # try:
        #     self.users = self._create_tables()
        # except Exception:
        #     pass

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
        for user in session.query(User).\
            filter(User.user_name == username):
            return user

    def find_user_with_email(self, email):
        """ Get a user by email"""
        session = self._get_session()
        for user in session.query(User).\
            filter(User.email_address == email):
            return user

    def get_studio(self, string):

        search_session = self._get_session()
        count = search_session.query(Studio).filter_by(studio_name=string).count()

        if count > 0:
            search_session.close()
            return True
        else:
            search_session.close()
            return False

    def populate_generic_data(self):
        """
        Populate Studio Table with Generic Tattoo Shops
        Note: this would be replaced with customer data/people who buy this software

        """
        save_session = self._get_session()
        # Create Studio object; use named args to set values of the object
        test_studio = Studio(studio_name='Rad Tattoo Shop', admin_email_address='jen.plemel@gmail.com',
                            studio_url='www.blackendtattoo.com/')
        # if it doesn't already exist
        if not (self.get_studio(test_studio.studio_name)):
            # Add testStudio object to session
            # This maps the object to a row in the DB
            save_session.add(test_studio)
            print('Added ' + test_studio.studio_name + ' to DB')
            # Doesn't save to DB until session is committed, or closed
            # Commit to save changes
        save_session.commit()


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