from flask import Flask, render_template, request, redirect, session
import time
from src.login import UserManager
from src.database import Database
from os import environ

app = Flask(__name__)
# __name__ helps determine root path

USER_MANAGER = UserManager()

# Secret Keys
# RuntimeError: The session is unavailable because no secret key was set.
# Set the secret_key on the application to something unique and secret.
# https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session
app.secret_key = 'pickle rick'
app.config['DEBUG'] = environ.get('env') != 'PROD'
app.config['TEMPLATES_AUTO_RELOAD'] = app.config['DEBUG']


# routing/mapping url to whatever web page you want to connect (return value)
# @ signifies a decorator - way to wrap a function and modifying it's behavior
@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def index():
    # First Page
    """ First Page/Login """
    # Makes sure we go to Home if user is logged in
    if check_for_user():
        # Direct to home if user is logged in
        print('User exists > Sending home')
        return redirect('/home')
    print('User does not exist, return to login')
    # User does not exist, return to index
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
@app.route('/login.html', methods=['GET'])
def auth():
    """ Authentication endpoint """
    # if the request is a post
    if request.method == 'POST':
        print('POST')
        # try and get the info entered
        username = request.form.get('username', None)
        print(username)
        password = request.form.get('password', None)
        print(password)
        # check if the user exists and the password matches
        if USER_MANAGER.validate_credentials(username, password):
            print('user login valid')
            # log the user in with the session
            sign_user_in(username)
            # send the user to the home page
            return redirect('/home')
        print('user login invalid')
        # send the user the login page with the error text
        return render_template('login.html', error_text="Invalid username or password")
    else:
        print('GET')
        if check_for_user():
            print('User is logged in, sending to home')
            return redirect('/home')
        print('User is not logged in, sending to login page @ Main Line 65')
        return render_template('login.html')


# TODO: Account creation page

# TODO: Home page: Request Appointment

# TODO: Appointment Page: Select Shop, Appointment specifications, Time Slot Selection, Submit Request

# TODO: If admin of tattoo shop... Requests (Accept/Deny + Confirmation Email), Manage Users, View Customers, etc...


@app.route('/home', methods=['GET', 'POST'])
def home():
    # User comes here if valid login
    """ This is the path in your application that users are redirected to after they have authenticated with Google """
    return render_template("home.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # User directed here from index, if link clicked
    """ New User Sign Up Page"""
    return render_template("signup.html")


# Code snippet from group project collaboration w/Robert, Stephanie, and Alex
def check_for_user():
    """
    - Check if a user has logged in
    - Refresh the expiration
    - If logged in, auto logout after 30 minutes of inactivity
    """

    try:
        # will throw a KeyError if it doesn't exist
        session_username = session['username']
        print('session_username %s' % session_username)
        # will throw a ValueError if not a number
        expiration = float(session['expiration'])
        print('session_expiration %s' % expiration)
        # get the current time in seconds
        current = time.time()
        print('current time %s' % current)
        # if the login has expired
        if current > expiration:
            print('current is greater than expiration, removing')
            # remove the user from the session
            sign_user_out()
            return False
        print('current is less than expiration, refreshing')
        # refresh the expiration to be 30 minutes from now
        add_expiration()
        return True
    except KeyError:
        print('No username in session')
        # if the username or expiration is not in the session
        return False
    except ValueError:
        print('expiration was not a valid float %s' % expiration)
        # if the expiration is not a valid float
        return False


def sign_user_in(username):
    """add the required information to the session for a signed in user"""
    session['username'] = username
    add_expiration()


def add_expiration():
    """Update or add the exxpiration to the session"""
    session['expiration'] = time.time() + (30 * 60)


def sign_user_out():
    """remove the information from the session to sign a user out"""
    del session['username']
    del session['expiration']


if __name__ == '__main__':

    # Setup Database
    db = Database()
    db.populate_generic_data()
    # Start this application
    app.run(debug=True, threaded=True)
