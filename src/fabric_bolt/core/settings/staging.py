# staging server settings for core project.

DEBUG = True

DATABASES = {
    'default': {
        # The last part of ENGINE is 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'ado_mssql'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',  # Or path to database file if using sqlite3
        'USER': '',             # Not used with sqlite3.
        'PASSWORD': '',         # Not used with sqlite3.
        'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',             # Set to empty string for default. Not used with sqlite3.
        'SCHEMA': '',
    }
}