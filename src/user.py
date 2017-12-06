from src.base import Base
from sqlalchemy import Column, String, Integer, create_engine


'''
---------------------------------------------------------
User Class: Represents a person + their user credentials
---------------------------------------------------------
'''

# '''Listen for DB connections to enforce Foreign Key constraints'''
# @event.listens_for(Engine, "connect")

# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


class User(Base):

    """ Defines metadata about a User table. Will create User objects from rows in this table """

    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String)
    email_address = Column(String)
    password = Column(String)

    def __init__(self, first_name, last_name, user_name, email_address, password, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.email_address = email_address
        self.password = password
        self.user_id = user_id

    def __repr__(self):
        """ Returns string representation of this object, helpful for debugging """

        return 'User: Id = {} Username = {} First Name = {} Last Name = {} Email = {} Password = {} '\
            .format(self.user_id, self.user_name, self.first_name, self.last_name, self.email_address, self.password)

    def __str__(self):
        return self.__repr__()


# update the DB schema to enforce foreign key constraints
engine = create_engine('sqlite:///data_store.db', echo=False)
Base.metadata.create_all(engine)
