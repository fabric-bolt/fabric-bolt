from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from fabric_bolt.hosts import models


class HostCreateForm(forms.ModelForm):
    class Meta:
        model = models.Host

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'name',
        ButtonHolder(
            Submit('submit', 'Create Host', css_class='button')
        )
    )


class HostUpdateForm(HostCreateForm):

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'name',
        ButtonHolder(
            Submit('submit', 'Update Host', css_class='button')
        )
    )