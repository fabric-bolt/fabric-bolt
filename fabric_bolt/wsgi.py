import os
import os.path
from django.conf import settings
from django.utils import autoreload

try:
    from uwsgidecorators import *
except:
    def timer(f): return f

try:
    import uwsgi
except ImportError:  # uwsgi module is available only when running inside uwsgi
    uwsgi = None

# Add the project to the python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
sys.stdout = sys.stderr

# Configure the application (Logan)
from fabric_bolt.utils.runner import configure

configure()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Load tasks
from core import tasks

if settings.DEBUG:
    @timer(2)
    def change_code_gracefull_reload(sig):
        if autoreload.code_changed() and uwsgi:
            uwsgi.reload()
