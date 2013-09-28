from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy

import models
import forms

class HostCreate(CreateView):
    model = models.Host
    form_class = forms.HostForm
    success_url = reverse_lazy('hosts_host_list')


class HostList(ListView):
    model = models.Host
