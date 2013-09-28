from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

import models


class ProjectCreateForm(forms.ModelForm):

    type = forms.ModelChoiceField(models.ProjectType.objects.all(), empty_label=None)

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


class ConfigurationCreateForm(forms.ModelForm):

    class Meta:
        model = models.Configuration
        fields = [
            'key',
            'value',
            'prompt_me_for_input',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        'key',
        'value',
        'prompt_me_for_input',
        ButtonHolder(
            Submit('submit', 'Create Configuration', css_class='button')
        )
    )


class ConfigurationUpdateForm(ConfigurationCreateForm):

    class Meta:
        model = models.Configuration
        fields = [
            'key',
            'value',
            'prompt_me_for_input',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        'key',
        'value',
        'prompt_me_for_input',
        ButtonHolder(
            Submit('submit', 'Update Configuration', css_class='button')
        )
    )


class DeploymentForm(forms.ModelForm):
    class Meta:
        fields = ['comments']
        model = models.Deployment

    helper = FormHelper()

    helper.layout = Layout(
        'comments',
        ButtonHolder(
            Submit('submit', 'Go!', css_class='btn btn-success')
        )
    )


class StageCreateForm(forms.ModelForm):

    class Meta:
        model = models.Stage
        fields = [
            'name',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        'name',
        ButtonHolder(
            Submit('submit', 'Create Stage', css_class='button')
        )
    )


class StageUpdateForm(StageCreateForm):

    class Meta:
        model = models.Stage
        fields = [
            'name',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        'name',
        ButtonHolder(
            Submit('submit', 'Update Stage', css_class='button')
        )
    )