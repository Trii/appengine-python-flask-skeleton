"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template
from flask.ext.security import Security, login_required
from flask_security_ndb import NDBUserDatastore, User, Role, send_email

app = Flask(__name__)
app.config.from_object('config.AppSettings')

# Setup Flask-Security using the NDB adapter stuff I wrote
user_datastore = NDBUserDatastore(User, Role)
security = Security(app, user_datastore)

# Override Flask-Mail by using the hook in :class:`flask_security.core._SecurityState`
security.send_mail_task(send_email)


@app.route('/')
@login_required
def home():
    """Return a friendly homepage."""
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
