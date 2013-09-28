from django.views.generic.edit import CreateView

import models

class CreateHost(CreateView):
    model = models.Host
