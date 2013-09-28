from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from custom_user.models import EmailUser
from django.utils.translation import ugettext_lazy as _

from .models import DeployUser
from .forms import UserChangeForm, UserCreationForm


class DeployUserAdmin(UserAdmin):

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff') #'first_name', 'last_name',

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', )
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register the new DeployUserAdmin
admin.site.register(DeployUser, DeployUserAdmin)