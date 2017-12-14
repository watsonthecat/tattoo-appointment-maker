# event = {
#         'summary': 'Google I/O 2015',
#         'location': '800 Howard St., San Francisco, CA 94103',
#         'description': 'A chance to hear more about Google\'s developer products.',
#         'start': {
#             'dateTime': '2015-05-28T09:00:00-07:00',
#             'timeZone': 'America/Los_Angeles',
#         },
#         'end': {
#             'dateTime': '2015-05-28T17:00:00-07:00',
#             'timeZone': 'America/Los_Angeles',
#         },
#         'recurrence': [
#             'RRULE:FREQ=DAILY;COUNT=2'
#         ],
#         'attendees': [
#             {'email': 'lpage@example.com'},
#             {'email': 'sbrin@example.com'},
#         ],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#             ],
#         },
#     }
from src.base import Base
from sqlalchemy import Column, String, Integer, create_engine



'''
--------------------------------------------------------------------
Booked Events Class:  For Events that have been added to Calendar
--------------------------------------------------------------------
'''


class Booked(Base):

    """ Defines metadata about an Events that have been booked table.
    Will create Event objects from rows in this table """

    __tablename__ = 'Booked'

    booked_id = Column(Integer, primary_key=True)
    studio_id = Column(Integer)
    event_id = Column(Integer)
    user_id = Column(Integer)
    summary = Column(String)
    location = Column(String)
    description = Column(String)
    start_datetime = Column(String)
    end_datetime = Column(String)
    timezone = Column(String)
    attendee_studio = Column(String)
    attendee_user = Column(String)

    def __init__(self, studio_id, event_id, user_id, summary, location, description, start_datetime, end_datetime, timezone,
                 attendee_studio, attendee_user):

        self.studio_id = studio_id
        self.event_id = event_id
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

        return 'Event: Booked Id = {} Studio Id = {} Event Id = {} User Id = {} Summary = {} Description = {} ' \
               'Start Time = {} ' 'End Time = {} ' \
               'Timezone = {} ' \
               ' Attendees = {} {} '\
            .format(self.booked_id, self.studio_id, self.event_id, self.user_id, self.summary, self.description,
                    self.start_datetime, self.end_datetime, self.timezone, self.attendee_studio, self.attendee_user)

    def __str__(self):
        return self.__repr__()


# update the DB schema to enforce foreign key constraints
engine = create_engine('sqlite:///data_store.db', echo=False)
Base.metadata.create_all(engine)
