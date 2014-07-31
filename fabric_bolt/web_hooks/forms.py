from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

from fabric_bolt.web_hooks import models


class HookCreateForm(forms.ModelForm):

    button_prefix = "Create"

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

            ButtonHolder(
                Submit('submit', '%s Hook' % self.button_prefix, css_class='button')
            )
        )

        super(HookCreateForm, self).__init__(*args, **kwargs)


class HookUpdateForm(HookCreateForm):

    button_prefix = "Update"