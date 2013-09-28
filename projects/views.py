from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy


from django_tables2.views import SingleTableView

import models
import forms
import tables


class ProjectList(SingleTableView):
    table_class = tables.ProjectTable
    model = models.Project


class ProjectCreate(CreateView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    template_name_suffix = '_create'

    def get_success_url(self):
        if self.success_url:
            url = self.success_url % self.object.__dict__
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")

        # Good to make note of that
        messages.add_message(self.request, messages.INFO, 'Project %s created' % self.object.name)

        return url


class ProjectUpdate(UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('projects_project_list')


class ProjectView(DetailView):
    model = models.Project
