from django.contrib.auth import get_user_model

from fabric_bolt.hosts.models import Host
from fabric_bolt.projects.models import Project


def sidebar_lists(request):
    context = {}
    if request.user.is_authenticated():
	    context['sidebar_hosts'] = Host.objects.all()
	    context['sidebar_projects'] = request.user.userproject_set.all()
	    context['sidebar_users'] = get_user_model().objects.all()
    return context