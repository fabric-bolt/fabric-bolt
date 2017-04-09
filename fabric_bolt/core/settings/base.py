# Global settings for core project.
import os

########## PATH CONFIGURATION
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(PROJECT_DIR, 'public')

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fabric_bolt.core.wsgi.application'
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
DEBUG = False
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## URL CONFIGURATION
ROOT_URLCONF = 'fabric_bolt.core.urls'
########## END URL CONFIGURATION


########## GENERAL CONFIGURATION

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Location of fixtures for the project
FIXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'fixtures'),
)
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'fabric_bolt.core.context_processors.sidebar_lists',
                'sekizai.context_processors.sekizai',
            ],
            'debug': False,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]

########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
]
########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION
INSTALLED_APPS = [
    # Django Core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # 3rd Party
    'django.contrib.admin',
    'sekizai',
    'crispy_forms',
    'stronghold',
    'django_tables2',
    'bootstrapform',
    'graphos',
    'django_activeurl',
    'authtools',

    # Project
    'fabric_bolt.accounts',
    'fabric_bolt.hosts',
    'fabric_bolt.launch_window',
    'fabric_bolt.projects',
    'fabric_bolt.web_hooks',
    'fabric_bolt.task_runners',
]
########## END APP CONFIGURATION

FABFILE_PATH = os.path.join(os.path.dirname(PROJECT_DIR), 'fabfile.py')

########## STRONGHOLD CONFIGURATION
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
STRONGHOLD_PUBLIC_NAMED_URLS = (
    'password_reset',
    'password_reset_done',
    'password_reset_complete',
    'business_redirect_setup',
)
STRONGHOLD_PUBLIC_URLS = (
    r'^/users/reset/[0-9A-Za-z_\-]+/[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/',
    r'^/api/v1/.*'
)
########## END STRONGHOLD CONFIGURATION


########## CRISPY CONFIGURATION
CRISPY_TEMPLATE_PACK = "bootstrap3"
########## END CRISPY CONFIGURATION


########## AUTH_USER_MODEL CONFIGURATION
AUTH_USER_MODEL = 'accounts.DeployUser'
########## END AUTH_USER_MODEL CONFIGURATION


########## EMAIL CONFIGURATION
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
########## END EMAIL CONFIGURATION


########## LOGGING CONFIGURATION
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PUBLIC_DIR, '.django_cache'),
    }
}

FABRIC_TASK_CACHE_TIMEOUT = 60 * 60 * 24  # one day

TASK_RUNNER_BACKEND = 'fabric_bolt.task_runners.basic.BasicStreamBackend'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "fabric_bolt.task_runners.channels.routing.channel_routing"
    },
}
