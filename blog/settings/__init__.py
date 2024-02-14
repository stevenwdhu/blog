from distutils.util import strtobool
from os import getenv

if strtobool(getenv('PRODUCTION_ENV', 'False')):
    from .production import *
else:
    from .development import *
