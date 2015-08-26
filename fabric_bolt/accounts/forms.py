import string
import random

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.
    """
    user_level = forms.ModelChoiceField(queryset=Group.objects.all())
    is_active = forms.ChoiceField(choices=((True, 'Active'), (False, 'Disabled')), label='Status')

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'user_level', 'is_active', 'template']

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

        if not user_is_admin:
            self.fields.pop('user_level', None)
            self.fields.pop('is_active', None)

        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def save(self, commit=True):
        """
        Save the model instance with the correct Auth Group based on the user_level question
        """
        instance = super(UserChangeForm, self).save(commit=commit)

        if commit:
            self.set_permissions(instance)

        return instance

    def set_permissions(self, instance):
        # Assign user to selected group
        if self.cleaned_data.get('user_level', False):
            instance.groups.clear()
            instance.groups.add(self.cleaned_data['user_level'])

        # Set staff status based on user group
        instance.is_staff = instance.user_is_admin()
        instance.save()


class UserCreationForm(UserChangeForm):
    """
    A form for creating new users. Includes all the required fields, plus a
    repeated password.
    """

    error_messages = {'duplicate_email': _("A user with that email already exists."), }

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

    def save(self, commit=True):
        """
        Save the model instance with the correct Auth Group based on the user_level question
        """
        instance = super(UserCreationForm, self).save(commit=commit)
        random_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
        instance.set_password(random_password)
        instance.save()

        email_form = PasswordResetForm({'email': self.cleaned_data['email']})
        email_form.is_valid()
        email_form.save(email_template_name='accounts/welcome_email.html')

        return instance
