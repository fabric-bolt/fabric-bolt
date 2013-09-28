from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages

from django_tables2.views import SingleTableView

import models
import forms
import tables


class HostCreate(CreateView):
    model = models.Host
    form_class = forms.HostCreateForm
    template_name_suffix = '_create'

    def form_valid(self, form):
        ret = super(HostCreate, self).form_valid(form)
        messages.success(self.request, 'Host {} Successfully Created'.format(self.object))
        return ret

    def get_success_url(self):
        return reverse('hosts_host_detail', kwargs={'pk': self.object.pk})


class HostList(SingleTableView):
    table_class = tables.HostTable
    model = models.Host


class HostUpdate(UpdateView):
    model = models.Host
    form_class = forms.HostUpdateForm
    template_name_suffix = '_update'

    def form_valid(self, form):
        ret = super(HostUpdate, self).form_valid(form)
        messages.success(self.request, 'Host {} Successfully Updated'.format(self.object))
        return ret

    def get_success_url(self):
        return reverse('hosts_host_detail', kwargs={'pk': self.object.pk})


class HostDetail(DetailView):
    model = models.Host


class HostDelete(DeleteView):
    model = models.Host
    success_url = reverse_lazy('hosts_host_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Host {} Successfully Deleted'.format(self.get_object()))
        return super(HostDelete, self).delete(self, request, *args, **kwargs)