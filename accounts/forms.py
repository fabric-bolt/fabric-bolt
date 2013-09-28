
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
    helper.layout = Layout(
        Fieldset(
            'Please Login',
            Field('username', css_class='input-xlarge'),
            Field('password', css_class='input-xlarge'),
        ),
        FormActions(
            Submit('login', 'Login', css_class="button"),
            HTML('<br/><a href="{% url \'password_recover\' %}">Recover Password</a>'),
        )
    )