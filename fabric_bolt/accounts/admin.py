from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from authtools.admin import UserAdmin

from fabric_bolt.accounts.forms import UserChangeForm, UserCreationForm


class UserChangeAdminFrom(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def __init__(self, *args, **kwargs):
        kwargs.update(user_is_admin=True)
        super(UserChangeAdminFrom, self).__init__(*args, **kwargs)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


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
        (_('Permissions'), {'fields': ( 'is_staff', 'is_superuser','user_level', 'is_active' )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', )
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', )
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def save_model(self, request, obj, form, change):
        super(DeployUserAdmin, self).save_model(request, obj, form, change)
        form.set_permissions(obj)

# Register the new DeployUserAdmin

# admin.site.register(get_user_model(), DeployUserAdmin)