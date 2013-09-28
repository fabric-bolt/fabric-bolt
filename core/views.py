from django.views.generic import TemplateView

from projects.models import Project


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):

        projects = Project.objects.all()

        return {
            'projects': projects,
        }