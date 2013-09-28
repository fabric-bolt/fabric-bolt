from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from django_tables2.views import SingleTableView

import models
import forms
import tables


class HostCreate(CreateView):
    model = models.Host
    form_class = forms.HostCreateForm
    success_url = reverse_lazy('hosts_host_list')
    template_name_suffix = '_create'


class HostList(SingleTableView):
    table_class = tables.HostTable
    model = models.Host


class HostUpdate(UpdateView):
    model = models.Host
    form_class = forms.HostUpdateForm
    success_url = reverse_lazy('hosts_host_list')
    template_name_suffix = '_update'
