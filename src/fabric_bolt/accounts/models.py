"""
Custom user model for deployments.
"""

import os
import urllib
import hashlib

from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

from custom_user.models import AbstractEmailUser
from custom_user.models import EmailUserManager


class UserManager(EmailUserManager):
    def get_query_set(self):
        qs = super(UserManager, self).get_query_set()
        return qs.prefetch_related('groups')


class DeployUser(AbstractEmailUser):
    """
    Custom user class for deployments. Email as username using django-custom-user.
    """

    AMELIA = 'amelia.min.css'
    CERULEAN = 'cerulean.min.css'
    COSMO = 'cosmo.min.css'
    CYBORG = 'cyborg.min.css'
    FLATLY = 'flatly.min.css'
    JOURNAL = 'journal.min.css'
    READABLE = 'readable.min.css'
    SIMPLEX = 'simplex.min.css'
    SLATE = 'slate.min.css'
    SPACELAB = 'spacelab.min.css'
    UNITED = 'united.min.css'
    YETI = 'yeti.min.css'

    TEMPLATES = (
        (AMELIA, 'Amelia'),
        (CERULEAN, 'Cerulean'),
        (COSMO, 'Cosmo'),
        (CYBORG, 'Cyborg'),
        (FLATLY, 'Flatly'),
        (JOURNAL, 'Journal'),
        (READABLE, 'Readable'),
        (SIMPLEX, 'Simplex'),
        (SLATE, 'Slate'),
        (SPACELAB, 'Spacelab'),
        (UNITED, 'United'),
        (YETI, 'Yeti'),
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    template = models.CharField(max_length=255, blank=True, choices=TEMPLATES, default=YETI)

    objects = UserManager()

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def user_is_admin(self):
        if not self.pk:
            return False

        for group in self.groups.all():
            if group.name == "Admin":
                return True

        return False

    def user_is_deployer(self):
        if not self.pk:
            return False

        for group in self.groups.all():
            if group.name == "Deployer":
                return True

        return False

    def user_is_historian(self):
        if not self.pk:
            return False

        for group in self.groups.all():
            if group.name == "Historian":
                return True

        return False

    def group_strigify(self):
        """
        Converts this user's group(s) to a string and returns it.
        """
        return "".join([group.name for group in self.groups.all()])

    def gravatar(self, size=20):
        """
        Construct a gravatar image address for the user
        """
        default = "mm"

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})

        return gravatar_url