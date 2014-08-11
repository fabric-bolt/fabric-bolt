from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FormActions

from fabric_bolt.launch_window import models


class LaunchWindowCreateForm(forms.ModelForm):

    class Meta:
        model = models.LaunchWindow
        fields = ['name', 'description', 'cron_format']

    # Form Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-4'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('name'),
        Field('description'),
        Field('cron_format'),
        FormActions(
            Submit('save', 'Save', css_class="button"),
        )
    )


class LaunchWindowUpdateForm(LaunchWindowCreateForm):
    pass