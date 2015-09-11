from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from fabric_bolt.hosts import models


class HostCreateForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = ['name', 'alias']

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'name',
        'alias',
        FormActions(
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
        'alias',
        FormActions(
            Submit('submit', 'Update Host', css_class='button')
        )
    )


class CreateSSHConfig(forms.Form):

    name = forms.CharField(max_length=255)
    public_key = forms.CharField(widget=forms.Textarea())
    private_key = forms.CharField(widget=forms.Textarea())
    remote_user = forms.CharField(max_length=255)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'name',
        'public_key',
        'private_key',
        'remote_user',
        FormActions(
            Submit('submit', 'Create SSH Key', css_class='button')
        )
    )
