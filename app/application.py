# -*- coding: utf-8 -*-
"""
.. module:: application
    :synopsis: Module with no side effects to import the main Flask application object
"""
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.AppSettings')
