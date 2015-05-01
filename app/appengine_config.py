"""
`appengine_config.py` is automatically loaded when Google App Engine
starts a new instance of your application. This runs before any
WSGI applications specified in app.yaml are loaded.
"""
import os
from google.appengine.ext import vendor

here = os.path.dirname(os.path.realpath(__file__))

# Third-party libraries are stored in "lib", vendoring will make
# sure that they are importable by the application.
vendor.add(os.path.join(here, 'lib'))

del here
