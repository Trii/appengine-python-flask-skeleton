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
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
