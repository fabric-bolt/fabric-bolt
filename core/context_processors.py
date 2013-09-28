from hosts.models import Host


def sidebar_lists(request):
    context = {}
    context['sidebar_hosts'] = Host.objects.all()
    return context