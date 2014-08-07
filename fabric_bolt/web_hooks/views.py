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
    Project List page
    """

    table_class = tables.HookTable
    model = models.Hook
    queryset = models.Project.active_records.all()


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

    def dispatch(self, request, *args, **kwargs):
        # if request.user.user_is_historian():
        #     self.template_name = "projects/historian_detail.html"

        return super(HookDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HookDetail, self).get_context_data(**kwargs)

        configuration_table = tables.ConfigurationTable(self.object.project_configurations(), prefix='config_')
        RequestConfig(self.request).configure(configuration_table)
        context['configurations'] = configuration_table

        stages = self.object.get_stages().annotate(deployment_count=Count('deployment'))
        context['stages'] = stages

        stage_table = tables.StageTable(stages, prefix='stage_')
        RequestConfig(self.request).configure(stage_table)
        context['stage_table'] = stage_table

        deployment_table = tables.DeploymentTable(models.Deployment.objects.filter(stage__in=stages).select_related('stage', 'task'), prefix='deploy_')
        RequestConfig(self.request).configure(deployment_table)
        context['deployment_table'] = deployment_table

        return context


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
