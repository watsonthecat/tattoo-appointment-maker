from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

''' If a class inherits Base, it will be mapped to DB (table created for object/class)'''

# Engine represents the core interface to the database
# The first argument is the url of the database

engine = create_engine('sqlite:///data_store.db', echo=False)

Base = declarative_base()
# All of the mapped classes inherit from this
