from django.db.models import Manager
from django.db.models import Q


class HookManager(Manager):

    def hooks(self, project):
        """ Look up the urls we need to post to"""

        return self.get_queryset().filter(
            Q(project=None) |
            Q(project=project)
        ).distinct('url')
