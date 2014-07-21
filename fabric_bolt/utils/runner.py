from logan.runner import run_app, configure_app

import sys
import base64
import os

KEY_LENGTH = 40


CONFIG_TEMPLATE = """

from fabric_bolt.core.settings.base import *

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': os.path.join(CONF_ROOT, 'fabric-bolt.db'),
        'USER': 'sqlite3',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SECRET_KEY = %(default_key)r

"""


def generate_settings():
    output = CONFIG_TEMPLATE % dict(
        default_key=base64.b64encode(os.urandom(KEY_LENGTH)),
    )

    return output


def configure():
    configure_app(
        project='fabric-bolt',
        default_config_path='~/.fabric-bolt/settings.py',
        default_settings='fabric_bolt.core.settings.base',
        settings_initializer=generate_settings,
        settings_envvar='FABRIC_BOLT_CONF',
    )


def main(progname=sys.argv[0]):
    run_app(
        project='fabric-bolt',
        default_config_path='~/.fabric-bolt/settings.py',
        default_settings='fabric_bolt.core.settings.base',
        settings_initializer=generate_settings,
        settings_envvar='FABRIC_BOLT_CONF',
    )

if __name__ == '__main__':
    main()
