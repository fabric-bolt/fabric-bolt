from hosts.models import Host


def main_lists(request):
    context = {}
    context['hosts'] = Host.objects.all()
    return context