import re

from django import forms
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from fabric_bolt.projects import models
from fabric_bolt.task_runners import backend


class ProjectCreateForm(forms.ModelForm):

    button_prefix = "Create"

    class Meta:
        model = models.Project
        fields = [
            'name',
            'description',
            'use_repo_fabfile',
            'repo_url',
            'fabfile_requirements',
        ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            'use_repo_fabfile',
            'repo_url',
            'fabfile_requirements',
            FormActions(
                Submit('submit', '%s Project' % self.button_prefix, css_class='button')
            )
        )

        super(ProjectCreateForm, self).__init__(*args, **kwargs)


class ProjectUpdateForm(ProjectCreateForm):

    button_prefix = "Update"

    def clean_repo_url(self):
        # should do some clean up if repo_url changed
        if "repo_url" in self.changed_data:
            backend.clean_obsolete_project_git(self.instance)
        return self.cleaned_data["repo_url"]


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
            'value_ssh_key',
            'task_argument',
            'task_name',
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
            'data_type',
            'key',
            'value',
            'value_number',
            'value_boolean',
            'value_ssh_key',
            'task_argument',
            'task_name',
            'prompt_me_for_input',
            'sensitive_value',
            FormActions(
                Submit('submit', '%s Configuration' % self.button_prefix, css_class='btn')
            )
        )

        super(ConfigurationUpdateForm, self).__init__(*args, **kwargs)

        self.fields['data_type'].required = True
        self.fields['value_boolean'].coerce = lambda x: x == 'True'

    def clean(self):
        cleaned_data = super(ConfigurationUpdateForm, self).clean()
        key = self.cleaned_data.get('key', None)
        task_argument = self.cleaned_data.get('task_argument', None)
        data_type = self.cleaned_data.get('data_type', None)
        task_name = self.cleaned_data.get('task_name', None)

        if task_argument:
            # valid python variable name. Since this will be a parameter name, we can be very strict.

            if key is not None and not re.match(r'^[a-zA-Z_]+[0-9a-zA-Z_]*$', key):
                self._errors["key"] = self.error_class(
                    ['Since you have marked this as a task argument, this must be a valid python variable name.']
                )
                del cleaned_data["key"]

            if data_type is not None and data_type != models.Configuration.STRING_TYPE:
                self._errors["data_type"] = self.error_class(
                    ['Since you have marked this as a task argument, it must be a string data type. '
                     'Unfortunately, fabric currently accepts only string data types as task arguments.']
                )
                del cleaned_data["data_type"]

            if task_name is None or len(task_name.strip()) == 0:
                self._errors["task_name"] = self.error_class(
                    ['Since you have marked this as a task argument, you must specify the task name.']
                )

                try:
                    del cleaned_data["task_name"]
                except:
                    pass  # doesnt matter
        else:
            self.cleaned_data["task_name"] = None

        return cleaned_data


class ConfigurationCreateForm(ConfigurationUpdateForm):

    button_prefix = "Create"


class DeploymentForm(forms.ModelForm):

    class Meta:
        fields = ['comments']
        model = models.Deployment

    def __init__(self, *args, **kwargs):
        super(DeploymentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            'comments',
            FormActions(
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
            FormActions(
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
