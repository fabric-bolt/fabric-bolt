
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, HTML
from crispy_forms.bootstrap import FormActions


class LoginForm(forms.Form):
    """
    Super simple login form
    """
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Form Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-4'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Fieldset(
            'Please Login',
            Field('email'),
            Field('password'),
        ),
        FormActions(
            Submit('login', 'Login', css_class="button"),
            #HTML('<br/><a href="{% url \'password_reset\' %}">Recover Password</a>'),
        )
    )