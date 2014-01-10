from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from fabric_bolt.accounts.models import DeployUser
from fabric_bolt.accounts.forms import UserChangeForm, UserCreationForm


class UserChangeAdminFrom(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def __init__(self, *args, **kwargs):
        super(UserChangeAdminFrom, self).__init__(*args, **kwargs)
        self.fields['user_level'].required = False


class DeployUserAdmin(UserAdmin):

    # The forms to add and change user instances
    form = UserChangeAdminFrom
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'is_staff', )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'template')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
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