import os
import sys
from django.core.wsgi import get_wsgi_application

path = os.path.realpath(os.path.dirname(__file__))
if not path in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'chimeproj.settings'
application = get_wsgi_application()
