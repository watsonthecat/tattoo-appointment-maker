from src.database import Database
from src.user import User
import bcrypt


""" Manage User Login"""


class UserManager:

    def __init__(self):
        self.database = Database()

    def add_user(self, first_name, last_name, username, email_address, password):
        """ Add User to DB """

        # hash password
        # password_hash = self.hash_password(password)

        if self.find_user(username, email_address) is None:
            user = User(first_name=first_name, last_name=last_name, user_name=username, email_address=email_address,
                        password=password)
            self.database.add_user(user)
        else:
            raise RuntimeError('User already exists')

    def hash_password(self, password):
        """ Password Hashing """
        # https://pypi.python.org/pypi/bcrypt/3.1.0
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def get_user_profile(self, username):
        """ Query DB + return user by user_name """
        user = self.database.get_user(username)
        return user

    def find_user(self, username, email):
        """ Query DB for user_name or email_address"""
        user = self.database.get_user(username)
        if user is not None:
            return user
        return self.database.find_user_with_email(email)

    def validate_credentials(self, username, password):
        """ Validate password matches DB password """
        print(username + ' login.py @45')

        user = self.database.get_user(username)
        print(username + ' login.py @48')

        if user is None:
            return False

        # does the password match the DB password
        if password == user.password:
            return True


