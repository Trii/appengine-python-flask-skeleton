"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import render_template
from application import app
from flask_security import login_required
from flask_security_ndb import send_email
from admin import admin_app, add_default_views
from security import security_app

security_app.init_app(app)
# Override Flask-Mail for Google App Engine by using the hook in :class:`flask_security.core._SecurityState`
security_app.send_mail_task(send_email)

admin_app.init_app(app)
add_default_views(admin_app)

# Create a user to test with
@app.before_first_request
def create_user():
    datastore = security_app.datastore
    user = datastore.create_user(email='admin@example.org', password='password')
    role = datastore.find_or_create_role(name='admin', description='The Admin role for admin fun')
    datastore.add_role_to_user(user, role)


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
