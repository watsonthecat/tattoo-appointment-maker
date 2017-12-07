from flask import Flask, render_template, request, redirect
from src.database import Database

app = Flask(__name__)
# __name__ helps determine root path


# routing/mapping url to whatever web page you want to connect (return value)
# @ signifies a decorator - way to wrap a function and modifying it's behavior

@app.route('/', methods=['GET', 'POST'])
def index():
    # First Page
    """ First Page/Login """

    # Login or Create Account
    # If Login: Check that user input is correct, continue to "Home" page
    # If Create Account: Go to Create Account Page, if user input valid then create user, redirect to Login
    return render_template("login.html")

# TODO: Account creation page

# TODO: Home page: Request Appointment

# TODO: Appointment Page: Select Shop, Appointment specifications, Time Slot Selection, Submit Request

# TODO: If admin of tattoo shop... Requests (Accept/Deny + Confirmation Email), Manage Users, View Customers, etc...


@app.route('/home', methods=['GET', 'POST'])
def home():
    # User comes here if valid login
    """ This is the path in your application that users are redirected to after they have authenticated with Google """
    return render_template("home.html")




if __name__ == '__main__':

    # Setup Database
    db = Database()
    db.populate_generic_data()
    # Start this application
    app.run(debug=True, threaded=True)
