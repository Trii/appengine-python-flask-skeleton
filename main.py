"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template
from flask.ext.security import Security, login_required
from flask_security_ndb import NDBUserDatastore, User, Role

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True

'''
TODO https://github.com/mattupstate/flask-security/issues/236
Turn off the register email by setting SEND_REGISTER_EMAIL = False
Register a handler for the flask_security.signals.user_registered signal
Send an email wherever you like in the signal handler
'''
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

# Setup Flask-Security
user_datastore = NDBUserDatastore(User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='josh@awesome.com', password='password')


@app.route('/')
@login_required
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
