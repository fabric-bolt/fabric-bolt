from hosts.models import Host
from projects.models import Project


def sidebar_lists(request):
    context = {}
    context['sidebar_hosts'] = Host.objects.all()
    context['sidebar_projects'] = Project.objects.all()
    return context