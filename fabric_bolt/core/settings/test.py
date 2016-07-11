# Local settings for core project.
from fabric_bolt.core.settings.base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

########## End Django Debug Toolbar Configuration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fabric_bolt_test',  # Or path to database file if using sqlite3.
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3(-(r&DUMMYKEYFIRJUNK@@#@#d=48-5p&(f'

if DEBUG:
    # Show emails in the console during developement.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
