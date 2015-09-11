from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse

from django.contrib import messages
from django_tables2.views import SingleTableView

from fabric_bolt.core.mixins.views import MultipleGroupRequiredMixin, GroupRequiredMixin
from fabric_bolt.hosts import models, tables, forms
from fabric_bolt.hosts.utils import create_ssh_config


class HostList(MultipleGroupRequiredMixin, SingleTableView):
    group_required = ['Admin', 'Deployer', ]
    table_class = tables.HostTable
    model = models.Host


class HostDetail(MultipleGroupRequiredMixin, DetailView):
    group_required = ['Admin', 'Deployer', ]
    model = models.Host


class HostCreate(MultipleGroupRequiredMixin, CreateView):
    """View for creating a host. Hosts let us know where we can shovel code to."""
    group_required = ['Admin', 'Deployer', ]
    model = models.Host
    form_class = forms.HostCreateForm
    template_name_suffix = '_create'

    def form_valid(self, form):
        """First call the parent's form valid then let the user know it worked."""

        form_valid_from_parent = super(HostCreate, self).form_valid(form)
        messages.success(self.request, 'Host {} Successfully Created'.format(self.object))

        return form_valid_from_parent

    def get_success_url(self):
        """Send them back to the detail view for that host"""

        return reverse('hosts_host_detail', kwargs={'pk': self.object.pk})


class HostUpdate(GroupRequiredMixin, UpdateView):
    group_required = 'Admin'
    model = models.Host
    form_class = forms.HostUpdateForm
    template_name_suffix = '_update'

    def form_valid(self, form):
        """First call the parent's form valid then let the user know it worked."""

        form_valid_from_parent = super(HostUpdate, self).form_valid(form)
        messages.success(self.request, 'Host {} Successfully Updated'.format(self.object))

        return form_valid_from_parent

    def get_success_url(self):
        """"""
        return reverse('hosts_host_detail', kwargs={'pk': self.object.pk})


class HostDelete(GroupRequiredMixin, DeleteView):
    group_required = 'Admin'
    model = models.Host
    success_url = reverse_lazy('hosts_host_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Host {} Successfully Deleted'.format(self.get_object()))
        return super(HostDelete, self).delete(self, request, *args, **kwargs)


class SSHConfig(TemplateView):
    template_name = 'hosts/ssh_config.html'

    def get_view(self, *args, **kwargs):
        return super(SSHConfig, self).get(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        """Create the SSH file & then return the normal get method..."""

        existing_ssh = models.SSHConfig.objects.all()

        if existing_ssh.exists():
            return self.get_view()

        remote_user = self.request.POST.get('remote_user', 'root')

        create_ssh_config(remote_user=remote_user)

        return self.get_view()

    def get_context_data(self, **kwargs):

        ssh_config = models.SSHConfig.objects.all()

        return {
            'ssh_config': ssh_config.first(),
        }


