import datetime


from django.http import HttpResponseRedirect
from django.db.models.aggregates import Count
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse


from django_tables2 import RequestConfig, SingleTableView

from fabric_bolt.core.mixins.views import MultipleGroupRequiredMixin

from fabric_bolt.web_hooks import forms, tables, models


class HookList(SingleTableView):
    """
    Hook List page
    """

    table_class = tables.HookTable
    model = models.Hook


class HookCreate(MultipleGroupRequiredMixin, CreateView):
    """
    Create a new project
    """
    group_required = ['Admin', 'Deployer', ]
    model = models.Hook
    form_class = forms.HookCreateForm
    template_name_suffix = '_create'

    def get_initial(self):

        initial = super(HookCreate, self).get_initial()

        initial['project'] = self.kwargs.get('project_id')

        return initial

    def form_valid(self, form):
        """After the form is valid lets let people know"""

        ret = super(HookCreate, self).form_valid(form)

        # Good to make note of that
        messages.add_message(self.request, messages.SUCCESS, 'Hook %s created' % self.object.url)

        return ret


class HookDetail(DetailView):
    """
    Display the Project Detail/Summary page: Configurations, Stages, and Deployments
    """

    model = models.Hook


class HookUpdate(MultipleGroupRequiredMixin, UpdateView):
    """
    Update a project
    """
    group_required = ['Admin', 'Deployer', ]
    model = models.Hook
    form_class = forms.HookUpdateForm
    template_name_suffix = '_update'
    # success_url = reverse_lazy('projects_project_list')


class HookDelete(MultipleGroupRequiredMixin, DeleteView):
    """
    Deletes a project by setting the Project's date_deleted. We save projects for historical tracking.
    """
    group_required = ['Admin', ]
    model = models.Hook

    def delete(self, request, *args, **kwargs):

        self.success_url = self.get_object().get_absolute_url()

        messages.add_message(request, messages.WARNING, 'Hook Successfully Deleted')

        return super(HookDelete, self).delete(request, *args, **kwargs)
