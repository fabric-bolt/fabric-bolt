from authtools.models import UserManager
from django.contrib.auth.models import Group


class DeployUserManager(UserManager):
    def create_user(self, email, password=None, **kwargs):
        user = super(DeployUserManager, self).create_user(email, password, **kwargs)

        try:
            # make sure there are no groups defined already.
            user.groups.clear()
            # just set as lowest level since we're not sure what you want.
            user.groups.add(Group.objects.get(name='Historian'))
        except Group.DoesNotExist:
            # oops. Somebody forgot to add a Historian group. Whatever. just continue.
            pass

        return user

    def create_superuser(self, **kwargs):
        user = super(DeployUserManager, self).create_superuser(**kwargs)

        try:
            # make sure there are no groups defined already.
            user.groups.clear()
            # Grab the admin group and assign it.
            user.groups.add(Group.objects.get(name='Admin'))
        except Group.DoesNotExist:
            # oops. Somebody forgot to add a Admin group. Whatever. just continue.
            pass

        return user