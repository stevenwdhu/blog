from socket import gethostname

if gethostname() == 'django-server':
    from .production import *
else:
    from .development import *

    