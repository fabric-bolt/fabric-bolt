from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django_tables2.views import SingleTableView

from fabric_bolt.core.mixins.views import MultipleGroupRequiredMixin
from fabric_bolt.launch_window import models, tables, forms


class LaunchWindowList(MultipleGroupRequiredMixin, SingleTableView):
    group_required = ['Admin', 'Deployer', ]
    table_class = tables.LaunchWindowTable
    model = models.LaunchWindow


class LaunchWindowDetail(MultipleGroupRequiredMixin, DetailView):
    group_required = ['Admin', 'Deployer', ]
    model = models.LaunchWindow


class LaunchWindowCreate(MultipleGroupRequiredMixin, CreateView):
    """View for creating a launch window."""
    group_required = ['Admin', 'Deployer', ]
    model = models.LaunchWindow
    form_class = forms.LaunchWindowCreateForm
    template_name_suffix = '_create'

    def form_valid(self, form):
        """First call the parent's form valid then let the user know it worked."""

        form_valid_from_parent = super(LaunchWindowCreate, self).form_valid(form)
        messages.success(self.request, 'Launch Window {} Successfully Created'.format(self.object))

        return form_valid_from_parent

    def get_success_url(self):
        """Send them back to the detail view for that launch window"""

        return reverse('launch_window_launchwindow_detail', kwargs={'pk': self.object.pk})


class LaunchWindowUpdate(MultipleGroupRequiredMixin, UpdateView):
    group_required = ['Admin', ]
    model = models.LaunchWindow
    form_class = forms.LaunchWindowUpdateForm
    template_name_suffix = '_update'

    def form_valid(self, form):
        """First call the parent's form valid then let the user know it worked."""

        form_valid_from_parent = super(LaunchWindowUpdate, self).form_valid(form)
        messages.success(self.request, 'Launch Window {} Successfully Updated'.format(self.object))

        return form_valid_from_parent

    def get_success_url(self):
        """"""
        return reverse('launch_window_launchwindow_detail', kwargs={'pk': self.object.pk})


class LaunchWindowDelete(MultipleGroupRequiredMixin, DeleteView):
    group_required = 'Admin'
    model = models.LaunchWindow
    success_url = reverse_lazy('launch_window_launchwindow_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Launch Window {} Successfully Deleted'.format(self.get_object()))
        return super(LaunchWindowDelete, self).delete(self, request, *args, **kwargs)