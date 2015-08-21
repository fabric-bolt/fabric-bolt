from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import FormActions

from fabric_bolt.web_hooks import models


class HookCreateForm(forms.ModelForm):

    button_prefix = "Create"
    project = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.Hook
        fields = [
            'project',
            'url',
        ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'project',
            'url',

            FormActions(
                Submit('submit', '%s Hook' % self.button_prefix, css_class='button')
            )
        )

        super(HookCreateForm, self).__init__(*args, **kwargs)

    def clean_project(self, *args, **kwargs):

        if not self.cleaned_data['project']:
            return None

        project = models.Project.objects.get(pk=int(self.cleaned_data['project']))

        return project


class HookUpdateForm(HookCreateForm):

    button_prefix = "Update"

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        instance = kwargs['instance']
        delete_url = reverse('hooks_hook_delete', args=(instance.pk,))

        self.helper.layout = Layout(
            'project',
            'url',

            FormActions(
                Submit('submit', '%s Hook' % self.button_prefix, css_class='button'),
                HTML('<a href="' + delete_url + '" class="btn btn-danger">Delete Hook</a>'),
            )
        )

        super(HookCreateForm, self).__init__(*args, **kwargs)