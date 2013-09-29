import string
import random

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, HTML, Div
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
            Field('email', placeholder='demo@worthwhile.com'),
            Field('password', placeholder='123456'),
        ),
        FormActions(
            Submit('login', 'Login', css_class="button pull-right"),
            #HTML('<br/><a href="{% url \'password_reset\' %}">Recover Password</a>'),
        )
    )


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.
    """
    user_level = forms.ChoiceField(choices=Group.objects.all().values_list(), label='User Level')
    is_active = forms.ChoiceField(choices=((True, 'Active'), (False, 'Disabled')), label='Status')

    # Form Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-4'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('email'),
        Field('first_name'),
        Field('last_name'),
        Field('user_level'),
        Field('is_active'),
        Field('template'),
        FormActions(
            Submit('btnSubmit', 'Submit', css_class="button btn-primary pull-right"),
        ),
    )

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        # form instance and initial values
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', {})
        user_is_admin = kwargs.pop('user_is_admin', False)

        # Set initial values for the non-model questions
        if instance:
            # Get user's group
            groups = instance.groups.all()
            initial['user_level'] = groups[0].id if groups.exists() else None

            # Map is_active question to model property
            initial['is_active'] = instance.is_active

        kwargs['initial'] = initial

        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['password'].required = False
        self.fields['last_login'].required = False
        self.fields['date_joined'].required = False
        self.fields['template'].required = False

        if not user_is_admin:
            self.fields.pop('user_level', None)
            self.fields.pop('is_active', None)

        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    ## Set the hidden inputs to the initial value since we don't want them hoodwinked

    def clean_password(self):
        return self.initial["password"]

    def clean_last_login(self):
        return self.initial["last_login"]

    def clean_date_joined(self):
        return self.initial["date_joined"]

    def save(self, commit=True):
        """
        Save the model instance with the correct Auth Group based on the user_level question
        """
        instance = super(UserChangeForm, self).save(commit=commit)

        if commit:
            instance.save()

            # Assign user to selected group
            if self.cleaned_data.get('user_level', False):
                instance.groups.clear()
                instance.groups.add(Group.objects.get(id=self.cleaned_data['user_level']))

            # Set staff status based on user group
            instance.is_staff = instance.user_is_admin()
            instance.save()

        return instance


class UserCreationForm(UserChangeForm):
    """
    A form for creating new users. Includes all the required fields, plus a
    repeated password.
    """

    error_messages = {'duplicate_email': _("A user with that email already exists."), }

    class Meta:
        model = get_user_model()

    def clean_date_joined(self):
        return now()

    def clean_last_login(self):
        return now()

    def clean_email(self):
        """
        Set a nicer error message than the ORM.
        """
        email = self.cleaned_data["email"]
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password(self):
        """
        Generate a random 32 char password for this user
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

    def save(self, commit=True):
        """
        Save the model instance with the correct Auth Group based on the user_level question
        """
        instance = super(UserCreationForm, self).save(commit=commit)
        instance.set_password(self.cleaned_data['password'])
        instance.save()

        return instance


class UserPasswordChangeForm(PasswordChangeForm):

    # Form Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-4'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('old_password'),
        Field('new_password1'),
        Field('new_password2'),
        FormActions(
            Submit('btnSubmit', 'Submit', css_class="button btn-primary pull-right"),
        ),
    )


class UserPasswordCreateForm(SetPasswordForm):

    # Form Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-4'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('new_password1'),
        Field('new_password2'),
        FormActions(
            Submit('btnSubmit', 'Submit', css_class="button btn-primary pull-right"),
        ),
    )