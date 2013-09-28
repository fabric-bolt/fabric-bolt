from django.views.generic import CreateView

import models


class CreateProject(CreateView):
    model = models.Project