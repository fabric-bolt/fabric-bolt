"""
This settings file is an example of what you need to do to use the channels backend.
"""

from .base import *

INSTALLED_APPS += ['channels']

TASK_RUNNER_BACKEND = 'fabric_bolt.task_runners.channels.ChannelsBackend'
