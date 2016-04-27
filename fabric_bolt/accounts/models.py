"""
Custom user model for deployments.
"""

import urllib
import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _

from authtools.models import AbstractEmailUser

from fabric_bolt.core import themes

from .managers import DeployUserManager


class DeployUser(AbstractEmailUser):
    """
    Custom user class for deployments. Email as username using django-custom-user.
    """

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    template = models.CharField(max_length=255, blank=True, choices=themes.TEMPLATE_THEMES, default=themes.YETI)

    objects = DeployUserManager()

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def role(self):
        """
        Assumes the user is only assigned to one role and return it
        """
        return self.group_strigify()

    def _get_groups(self):
        if not hasattr(self, '_cached_groups'):
            self._cached_groups = list(self.groups.values_list("name", flat=True))
        return self._cached_groups

    def user_is_admin(self):
        if not self.pk:
            return False
        return "Admin" in self._get_groups()

    def user_is_deployer(self):
        if not self.pk:
            return False
        return "Deployer" in self._get_groups()

    def user_is_historian(self):
        if not self.pk:
            return False
        return "Historian" in self._get_groups()

    def group_strigify(self):
        """
        Converts this user's group(s) to a string and returns it.
        """
        return "/".join(self._get_groups())

    def gravatar(self, size=20):
        """
        Construct a gravatar image address for the user
        """
        default = "mm"

        gravatar_url = "//www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})

        return gravatar_url
