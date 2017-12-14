from flask import Flask, render_template, request, redirect, session
import time
from src.login import UserManager
from src.database import Database
from config import Keys
from src.user import User
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


@app.route('/adminlogin', methods=['GET','POST'])
def admin_auth():
    """ Authentication endpoint """
    # if the request is a post
    if request.method == 'POST':
        print('POST')
        # try and get the info entered
        username = request.form.get('username', None)
        print(username)
        password = request.form.get('password', None)
        print(password)
        studio_name = request.form.get('studio-name', None)
        # check if the user exists and the password matches
        if USER_MANAGER.check_if_admin(username, password, studio_name):
            print('admin login valid')
            # log the user in with the session
            sign_user_in(username)
            # send the user to the home page
            return redirect('/adminhome')
        print('admin login invalid')
        # send the user the login page with the error text
        return render_template('adminlogin.html', error_text="Invalid username or password")
    else:
        print('GET')
        if check_for_user():
            print('Admin is logged in, sending to adminhome')
            return redirect('/adminhome')
        print('User is not logged in, sending to login page @ Main Line 65')
        return render_template('adminlogin.html')


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


@app.route('/signout', methods=['get'])
def sign_out():
    """ Sign Out the User"""
    if check_for_user():
        print('user logged in, signing out')
        sign_user_out()
        print('redirecting to index')
        return redirect('/')


# Appointment Page: Appointment specifications, Time Slot Selection, Submit Request
@app.route('/requestappointment', methods=['POST', 'GET'])
def request_appointment():
    """ Get event description from user + availability """

    if request.method == 'POST':
        print('POST')

        # Get appointment time
        time_slot_chosen = request.form.get('availability')

        print(time_slot_chosen)

        #TODO:Make this an update function so admin can set date of appointment
        year = '2017-'
        month = '12-'
        day = '14'
        date = year+month+day
        # Check if 12-4 or 4-8 and set variable
        if 'FirstAppointment' in time_slot_chosen:
            # Set vars to 12 & 4
            # Set appointment time 12-4pm
            time_start_noon = 'T12:00:00-06:00'
            time_end_four = 'T16:00:00-06:00'

            # 12-4pm start & end datetimes
            start_datetime = date + time_start_noon
            end_datetime = date + time_end_four

        elif 'SecondAppointment' in time_slot_chosen:
            # Set vars to 4 & 8
            # Set appointment time 4-8pm
            time_start_four = 'T16:00:00-06:00'
            time_end_eight = 'T20:00:00-06:00'

            # 4-8pm start & end datetimes
            start_datetime = date + time_start_four
            end_datetime = date + time_end_eight

        username = session['username']
        user = USER_MANAGER.get_user_profile(username)
        studio = USER_MANAGER.get_studio_profile('Rad Tattoo Shop')
        user_id = user.user_id
        summary = user.first_name + ' ' + user.last_name + ' Tattoo Appointment'
        location = studio.studio_name
        tattoo = request.form.get('tattoo')
        tattoo_size = request.form.get('tattoo-size')
        tattoo_location = request.form.get('tattoo-location')
        description = 'Email: '+user.email_address + " " + 'Tattoo: ' + tattoo + " " + 'Size: ' + tattoo_size + " "\
                      + 'Tattoo Location: ' + tattoo_location + " "

        timezone = 'America/Chicago'
        attendee_studio = studio.admin_email_address
        # This will use the user's email address
        # attendee_user = user.email_address
        ''' Using my other email for testing/until actual launch '''
        # this would be replaced with user.email_address to actually invite the user
        attendee_user = Keys.testuser_email

        try:
            USER_MANAGER.add_event(user_id, summary, location, description, start_datetime, end_datetime, timezone,
                                   attendee_studio, attendee_user)
            sign_user_in(username)
            print('event created')
        except RuntimeError as err:
            print('failed to complete appointment request')
            return render_template('requestappointment.html', error_text=err.args[0])
        print('redirecting to home')
        return redirect('/home')

    print('sending signup')
    return render_template("requestappointment.html")


@app.route('/home', methods=['GET', 'POST'])
def home():
    # User comes here if valid login
    """ This is the path in your application that users are redirected to after they have authenticated with Google """
    # Get user profile
    if request.method == 'GET':
        print('GET')
        if check_for_user():
            username = session['username']
            print(username)
            user = USER_MANAGER.get_user_profile(username)
            print(user)
            # To Show Appointment Requests
            event_list = USER_MANAGER.event_list_by_id(user.user_id)

            if user is None:
                return render_template('home.html', error='Unable to find user')
            return render_template('home.html', user=user, event_list=event_list)


@app.route('/delStuff', methods=['POST'])
def del_stuff():

    print(request.form)
    event_id = request.form.get('event-id')

    if not event_id is None:
        pass

    if request.method == 'POST':
        if request.form['submit'] == 'del_event_btn':
            USER_MANAGER.delete_event(event_id)
        else:
            pass  # unknown

    return redirect("/home")


@app.route('/adminhome', methods=['GET', 'POST'])
def admin_home():
    if request.method == 'GET':
        print('GET')
        if check_for_user():
            username = session['username']
            print(username)
            user = USER_MANAGER.get_user_profile(username)
            print(user)
            studio = USER_MANAGER.get_studio_profile('Rad Tattoo Shop')
            # To Show Appointment Requests
            event_list = USER_MANAGER.event_list()
            # To Show Booked Appointments
            booked_list = USER_MANAGER.booked_list()

            if user is None:
                return render_template('adminhome.html', error='Unable to find user')

            return render_template('adminhome.html', user=user, event_list=event_list, studio=studio, booked_list=booked_list)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # User directed here from index, if link clicked
    """ New User Sign Up Page"""
    if request.method == 'POST':
        print('POST')
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')

        try:
            USER_MANAGER.add_user(first_name, last_name, username, email, password)
            sign_user_in(username)
            print('user created')
        except RuntimeError as err:
            print('failed to create user')
            return render_template('signup.html', error_text=err.args[0])
        print('redirecting to home')
        return redirect('/home')

    print('sending signup')
    return render_template("signup.html")


@app.route('/makeevent', methods=['POST'])
def make_event():
    """ Add to Calendar Button from adminhome.html """
    event_description = request.form.get('event-description')

    if request.method == 'POST':
        # If the Add to Calendar event button is pressed...
        if request.form['submit'] == 'make_event_btn':
            # Get event associated with button
            event = USER_MANAGER.find_event(event_description)
            # Add event to Calendar
            USER_MANAGER.add_to_calendar(event)
            # Add booked event to Booked DB
            # var for studio id
            studio_id = '1'
            USER_MANAGER.add_booked(event, studio_id)
            # Remove Event from DB
            USER_MANAGER.delete_event(event.event_id)

        return redirect("/adminhome")


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
    """Update or add the expiration to the session"""
    session['expiration'] = time.time() + (30 * 60)


def sign_user_out():
    """remove the information from the session to sign a user out"""
    del session['username']
    del session['expiration']


if __name__ == '__main__':

    # Setup Database
    db = Database()
    db.populate_generic_data()
    db.populate_generic_user()
    # Start this application
    app.run(debug=True, threaded=True)
