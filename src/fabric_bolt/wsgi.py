import os
import os.path
import sys

# Add the project to the python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
sys.stdout = sys.stderr

# Configure the application (Logan)
from fabric_bolt.utils.runner import configure
configure()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()