from django import forms
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from fabric_bolt.projects import models


class ProjectCreateForm(forms.ModelForm):

    type = forms.ModelChoiceField(models.ProjectType.objects.all(), empty_label=None)
    button_prefix = "Create"

    class Meta:
        model = models.Project
        fields = [
            'name',
            'type',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'type',
            'description',
            ButtonHolder(
                Submit('submit', '%s Project' % self.button_prefix, css_class='button')
            )
        )

        super(ProjectCreateForm, self).__init__(*args, **kwargs)


class ProjectUpdateForm(ProjectCreateForm):

    button_prefix = "Update"


class ConfigurationUpdateForm(forms.ModelForm):

    button_prefix = "Update"

    class Meta:
        model = models.Configuration
        fields = [
            'key',
            'data_type',
            'value',
            'value_number',
            'value_boolean',
            'prompt_me_for_input',
            'sensitive_value',
        ]
        widgets = {'value_boolean': forms.Select(choices=((False, 'False'), (True, 'True')))}

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'key',
            'data_type',
            'value',
            'value_number',
            'value_boolean',
            'prompt_me_for_input',
            'sensitive_value',
            ButtonHolder(
                Submit('submit', '%s Configuration' % self.button_prefix, css_class='btn')
            )
        )

        super(ConfigurationUpdateForm, self).__init__(*args, **kwargs)

        self.fields['data_type'].required = True
        self.fields['value_boolean'].coerce = lambda x: x == 'True'


class ConfigurationCreateForm(ConfigurationUpdateForm):

    button_prefix = "Create"

    def __init__(self, *args, **kwargs):
        super(ConfigurationCreateForm, self).__init__(*args, **kwargs)

        self.fields['key'].validators.append(RegexValidator(r'^[a-zA-Z_]+[0-9a-zA-Z_]*$')) # valid python variable name


class DeploymentForm(forms.ModelForm):

    class Meta:
        fields = ['comments']
        model = models.Deployment

    def __init__(self, *args, **kwargs):
        super(DeploymentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            'comments',
            ButtonHolder(
                Submit('submit', 'Go!', css_class='btn btn-success')
            )
        )


class StageCreateForm(forms.ModelForm):
    button_prefix = "Create"

    class Meta:
        model = models.Stage
        fields = [
            'name',
        ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            ButtonHolder(
                Submit('submit', '%s Stage' % self.button_prefix, css_class='button')
            )
        )

        super(StageCreateForm, self).__init__(*args, **kwargs)


class StageUpdateForm(StageCreateForm):
    button_prefix = "Update"

    class Meta:
        model = models.Stage
        fields = [
            'name',
        ]