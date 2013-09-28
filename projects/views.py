from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy

from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView

import models
import forms
import tables


class BaseGetProjectCreateView(CreateView):

    def dispatch(self, request, *args, **kwargs):

        # Lets set the project so we can use it later
        project_id = kwargs.get('project_id')
        self.project = models.Project.objects.get(pk=project_id)

        return super(BaseGetProjectCreateView, self).dispatch(request, *args, **kwargs)


class ProjectList(SingleTableView):
    table_class = tables.ProjectTable
    model = models.Project


class ProjectCreate(CreateView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    template_name_suffix = '_create'

    def form_valid(self, form):
        """After the form is valid lets let people know"""

        ret = super(ProjectCreate, self).form_valid(form)

        # Good to make note of that
        messages.add_message(self.request, messages.SUCCESS, 'Project %s created' % self.object.name)

        return ret


class ProjectUpdate(UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('projects_project_list')


class ProjectView(DetailView):
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)

        configuration_table = tables.ConfigurationTable(self.object.configuration_set.all())
        RequestConfig(self.request).configure(configuration_table)
        context['configurations'] = configuration_table

        return context


class ProjectConfigurationCreate(BaseGetProjectCreateView):
    model = models.Configuration
    template_name_suffix = '_create'
    form_class = forms.ConfigurationCreateForm

    #def dispatch(self, request, *args, **kwargs):
    #
    #    # Lets set the project so we can use it later
    #    project_id = kwargs.get('project_id')
    #    self.project = models.Project.objects.get(pk=project_id)
    #
    #    return super(ProjectConfigurationCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Set the project on this configuration after it's valid"""

        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.save()

        # Good to make note of that
        messages.add_message(self.request, messages.SUCCESS, 'Configuration %s created' % self.object.key)

        return super(ProjectConfigurationCreate, self).form_valid(form)


class ProjectConfigurationUpdate(UpdateView):
    model = models.Configuration
    template_name_suffix = '_update'
    form_class = forms.ConfigurationUpdateForm


class ProjectStageCreate(BaseGetProjectCreateView):
    model = models.Stage
    template_name_suffix = '_create'
    form_class = forms.StageCreateForm

    def form_valid(self, form):
        """Set the project on this configuration after it's valid"""

        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.save()

        # Good to make note of that
        messages.add_message(self.request, messages.SUCCESS, 'Stage %s created' % self.object.name)

        return super(ProjectStageCreate, self).form_valid(form)


class ProjectStageView(DetailView):
    model = models.Stage

