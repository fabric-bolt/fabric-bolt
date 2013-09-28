from core.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tmp:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}