import time

from django.core.exceptions import ImproperlyConfigured
from django.http import StreamingHttpResponse
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

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

        stages = models.Stage.objects.all()

        context['stages'] = stages

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


class DeploymentCreate(CreateView):
    model = models.Deployment
    form_class = forms.DeploymentForm

    def dispatch(self, request, *args, **kwargs):
        self.stage = get_object_or_404(models.Stage, pk=int(kwargs['pk']))

        return super(DeploymentCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.stage = self.stage
        self.object.save()

        return super(DeploymentCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DeploymentCreate, self).get_context_data(**kwargs)
        context['stage'] = self.stage
        return context

    def get_success_url(self):
        return reverse('projects_deployment_detail', kwargs={'pk': self.object.pk})


class DeploymentDetail(DetailView):
    model = models.Deployment


class DeploymentOutputStream(View):

    def output_stream_generator(self):
        for x in range(1,11):
            yield '{} <br /> {}'.format(x, ' '*1024)
            time.sleep(1)

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(models.Deployment, pk=int(kwargs['pk']))
        resp = StreamingHttpResponse(self.output_stream_generator())
        return resp


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
