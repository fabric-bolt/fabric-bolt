import time
import datetime
import subprocess
import sys
from fabric.main import find_fabfile, load_fabfile, _task_names


from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, View, DeleteView
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
    queryset = models.Project.active_records.all()


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


class ProjectDelete(DeleteView):
    model = models.Project

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.date_deleted = datetime.datetime.now()
        self.object.save()

        messages.add_message(request, messages.WARNING, 'Project {} Successfully Deleted'.format(self.object))
        return HttpResponseRedirect(reverse('projects_project_list'))


class ProjectUpdate(UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('projects_project_list')


class ProjectView(DetailView):
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)

        configuration_table = tables.ConfigurationTable(self.object.project_configurations())
        RequestConfig(self.request).configure(configuration_table)
        context['configurations'] = configuration_table

        stages = self.object.stage_set.all()

        context['stages'] = stages

        deployment_table = tables.DeploymentTable(models.Deployment.objects.filter(stage__in=stages))
        RequestConfig(self.request).configure(deployment_table)
        context['deployment_table'] = deployment_table

        return context


class ProjectConfigurationCreate(BaseGetProjectCreateView):
    model = models.Configuration
    template_name_suffix = '_create'
    form_class = forms.ConfigurationCreateForm

    def form_valid(self, form):
        """Set the project on this configuration after it's valid"""

        self.object = form.save(commit=False)
        self.object.project = self.project

        if self.kwargs.get('stage_id', None):
            current_stage = models.Stage.objects.get(pk=self.kwargs.get('stage_id'))
            self.object.stage = current_stage

        self.object.save()

        # Good to make note of that
        messages.add_message(self.request, messages.SUCCESS, 'Configuration %s created' % self.object.key)

        return super(ProjectConfigurationCreate, self).form_valid(form)

    def get_success_url(self):
        success_url = super(ProjectConfigurationCreate, self).get_success_url()

        if self.object.stage:
            success_url = reverse('projects_stage_view', args=(self.object.pk, self.object.stage.pk))

        return success_url


class ProjectConfigurationUpdate(UpdateView):
    model = models.Configuration
    template_name_suffix = '_update'
    form_class = forms.ConfigurationUpdateForm


class ProjectConfigurationDelete(DeleteView):
    model = models.Configuration

    def dispatch(self, request, *args, **kwargs):

        return super(ProjectConfigurationDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Get the url depending on what type of configuration I deleted."""
        
        if self.stage_id:
            url = reverse('projects_stage_view', args=(self.project_id, self.stage_id))
        else:
            url = reverse('projects_project_view', args=(self.project_id))

        return url

    def delete(self, request, *args, **kwargs):

        obj = self.get_object()

        # Save where I was before I go an delete myself
        self.project_id = obj.project.pk
        self.stage_id = obj.stage.pk if obj.stage else None

        messages.success(self.request, 'Configuration {} Successfully Deleted'.format(self.get_object()))
        return super(ProjectConfigurationDelete, self).delete(self, request, *args, **kwargs)


class DeploymentCreate(CreateView):
    model = models.Deployment
    form_class = forms.DeploymentForm

    def dispatch(self, request, *args, **kwargs):
        self.stage = get_object_or_404(models.Stage, pk=int(kwargs['pk']))

        return super(DeploymentCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.stage = self.stage

        self.object.task, created = models.Task.objects.get_or_create(name=self.kwargs['task_name'])
        if not created:
            self.object.task.times_used += 1
            self.object.task.save()

        self.object.user = self.request.user
        self.object.save()

        return super(DeploymentCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DeploymentCreate, self).get_context_data(**kwargs)
        context['stage'] = self.stage
        context['task_name'] = self.kwargs['task_name']
        return context

    def get_success_url(self):
        return reverse('projects_deployment_detail', kwargs={'pk': self.object.pk})


class DeploymentDetail(DetailView):
    model = models.Deployment


class DeploymentOutputStream(View):

    def output_stream_generator(self):
        process = subprocess.Popen('ls -l /*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        all_output = ''
        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() != None:
                yield '<span id="finished"></span> {}'.format(' '*1024)
                break

            all_output += nextline
            yield '<span style="color:rgb(200, 200, 200);font-size: 14px;font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif;">$ {} </span><br /> {}'.format(nextline, ' '*1024)
            sys.stdout.flush()

        self.object.status = self.object.SUCCESS if process.returncode == 0 else self.object.FAILED
        self.object.output = all_output
        self.object.save()

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(models.Deployment, pk=int(kwargs['pk']), status=models.Deployment.PENDING)
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


class ProjectStageUpdate(UpdateView):
    model = models.Stage
    template_name_suffix = '_update'
    form_class = forms.StageUpdateForm


class ProjectStageView(DetailView):
    model = models.Stage

    def get_context_data(self, **kwargs):

        context = super(ProjectStageView, self).get_context_data(**kwargs)

        configuration_table = tables.ConfigurationTable(self.object.stage_configurations())
        RequestConfig(self.request).configure(configuration_table)
        context['configurations'] = configuration_table

        try:
            docstring, callables, default = load_fabfile(find_fabfile(None))
            all_tasks = sorted(_task_names(callables))
        except Exception as e:
            messages.error(self.request, 'Error loading fabfile: ' + e.message)
            all_tasks = []

        context['all_tasks'] = all_tasks
        context['frequent_tasks_run'] = models.Task.objects.filter(name__in=all_tasks).order_by('-times_used')[:3]

        return context
