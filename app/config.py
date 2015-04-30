# -*- coding: utf-8 -*-
"""
.. module:: config
   :synopsis: App config settings

The :mod:`<config>` module stores configuration settings for the app

"""

class AppSettings(object):
    """TODO: env settings?"""
    DEBUG = True
    SECRET_KEY = 'omg this is my secret key'

    # From on https://pythonhosted.org/passlib/new_app_quickstart.html#sha512-crypt
    # "`sha512_crypt` is probably the best choice for Google App Engine, as Google’s production
    # servers appear to provide native support via crypt, which will be used by Passlib."
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = ('F84EBDDCADDDA0BE84ADEDDA6E4AA8B2'
                              'C599B5A87C494ADBB9C8DE04480CD665'
                              'D105C4AD85812CCFAA9F55870BCDF3E5'
                              '5ABEA43377EFCE963E0FC79DB2D682EA')
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True

    # SECURITY_EMAIL_SUBJECT_REGISTER = ''
    # SECURITY_EMAIL_SUBJECT_PASSWORDLESS = ''
    # SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = ''
    # SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = ''
    # SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = ''
    # SECURITY_EMAIL_SUBJECT_CONFIRM = ''
