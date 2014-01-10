from django.contrib.auth import get_user_model

from fabric_bolt.hosts.models import Host
from fabric_bolt.projects.models import Project


def sidebar_lists(request):
    context = {}
    context['sidebar_hosts'] = Host.objects.all()
    context['sidebar_projects'] = Project.objects.all()
    context['sidebar_users'] = get_user_model().objects.all()
    return context