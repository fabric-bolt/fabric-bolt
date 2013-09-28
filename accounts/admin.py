from django.contrib import admin

from custom_user.admin import EmailUserAdmin

from .models import DeployUser
from .forms import UserChangeForm, UserCreationForm


class DeployUserAdmin(EmailUserAdmin):

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm


# Register the new DeployUserAdmin
admin.site.register(DeployUser, DeployUserAdmin)