
from src.base import Base
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey



'''
---------------------------------------------------------
Event Class: Represents a google calendar event
---------------------------------------------------------
'''

class Event(Base):

    """ Defines metadata about an Event table. Will create Event objects from rows in this table """

    __tablename__ = 'Event'

    event_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    summary = Column(String)
    location = Column(String)
    description = Column(String)
    start_datetime = Column(String)
    end_datetime = Column(String)
    timezone = Column(String)
    attendee_studio = Column(String)
    attendee_user = Column(String)

    def __init__(self, user_id, summary, location, description, start_datetime, end_datetime, timezone,
                 attendee_studio, attendee_user):

        self.user_id = user_id
        self.summary = summary
        self.location = location
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.timezone = timezone
        self.attendee_studio = attendee_studio
        self.attendee_user = attendee_user

    def __repr__(self):
        """ Returns string representation of this object, helpful for debugging """

        return 'Event: Event Id = {} User Id = {} Summary = {} Description = {} Start Time = {} End Time = {} ' \
               'Timezone = {} ' \
               ' Attendees = {} {} '\
            .format(self.event_id, self.user_id, self.summary, self.description, self.start_datetime, self.end_datetime,
                    self.timezone, self.attendee_studio, self.attendee_user)

    def __str__(self):
        return self.__repr__()


# update the DB schema to enforce foreign key constraints
engine = create_engine('sqlite:///data_store.db', echo=False)
Base.metadata.create_all(engine)
