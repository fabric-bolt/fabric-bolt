from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

import models


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'name',
            'type',
            'description',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        'name',
        'type',
        'description',
        ButtonHolder(
            Submit('submit', 'Create Project', css_class='button')
        )
    )


class ProjectUpdateForm(ProjectCreateForm):

    helper = FormHelper()
    helper.layout = Layout(
        'name',
        'type',
        'description',
        ButtonHolder(
            Submit('submit', 'Update Project', css_class='button')
        )
    )