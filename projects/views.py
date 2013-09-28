from django.core.exceptions import ImproperlyConfigured
from django.views.generic import CreateView, UpdateView

from django_tables2.views import SingleTableView

import models
import tables


class ProjectList(SingleTableView):
    table_class = tables.ProjectTable
    model = models.Project


class ProjectCreate(CreateView):
    model = models.Project

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
        return url


class ProjectUpdate(UpdateView):
    model = models.Project