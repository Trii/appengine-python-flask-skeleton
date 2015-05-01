# -*- coding: utf-8 -*-
"""
.. module:: security
    :synopsis: Setup of Flask-Security plugin
"""
from flask_security import Security
from flask_security_ndb import NDBUserDatastore, User, Role

class WrappedSecurity(Security):
    """Apply bug fix to init_app until #317 is mergerd

    See https://github.com/mattupstate/flask-security/pull/317
    """
    def init_app(self, app, datastore=None, register_blueprint=True, login_form=None, confirm_register_form=None,
                 register_form=None, forgot_password_form=None, reset_password_form=None, change_password_form=None,
                 send_confirmation_form=None, passwordless_login_form=None):

        self._state = super(WrappedSecurity, self).init_app(app, datastore, register_blueprint, login_form,
                                                            confirm_register_form, register_form, forgot_password_form,
                                                            reset_password_form, send_confirmation_form,
                                                            passwordless_login_form)

# Setup Flask-Security using the NDB adapter stuff I wrote
user_datastore = NDBUserDatastore(User, Role)
security_app = WrappedSecurity(datastore=user_datastore)
