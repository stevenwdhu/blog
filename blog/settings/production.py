from .base import *

INSTALLED_APPS += [
    'gunicorn',
]

DATABASES = dict(default=config['DATABASE'])

ALLOWED_HOSTS += config.get('ALLOWED_HOSTS')

DEBUG = False