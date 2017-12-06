from src.base import Base
from sqlalchemy import Column, String, Integer, create_engine

'''
---------------------------------------------------------
User Shop: Represents a tattoo studio + shop specifics
---------------------------------------------------------
'''


class Studio(Base):
    """ Defines metadata about a Shop table. Will create Shop objects from rows in this table """

    __tablename__ = 'studios'

    studio_id = Column(Integer, primary_key=True)
    studio_name = Column(String)
    admin_email_address = Column(String)  # Might be making this a foreign key
    studio_url = Column(String)

    def __init__(self, studio_name, admin_email_address,studio_url):
        self.studio_name = studio_name
        self.admin_email_address = admin_email_address
        self.studio_url = studio_url

    def __repr__(self):
        """ Returns string representation of this object, helpful for debugging """

        return 'Tattoo Studio: Id = {} Name = {} Admin Email = {} URL = {} ' \
            .format(self.studio_id, self.studio_name, self.admin_email_address, self.studio_url)

    def __str__(self):
        return self.__repr__()


# update the DB schema to enforce foreign key constraints
engine = create_engine('sqlite:///data_store.db', echo=False)
Base.metadata.create_all(engine)
