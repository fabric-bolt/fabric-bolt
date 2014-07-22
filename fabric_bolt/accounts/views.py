"""
Deployment User Views
"""

from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView

from authtools.views import PasswordChangeView
from django_tables2 import SingleTableView

from fabric_bolt.core.mixins.views import MultipleGroupRequiredMixin
from fabric_bolt.accounts import forms, tables


class UserPermissions(TemplateView):
    template_name = 'accounts/permissions.html'


# Admin: List Users
class UserList(MultipleGroupRequiredMixin, SingleTableView):
    """
    List of users. Uses UserFilter and UserTable.
    """
    group_required = 'Admin'
    template_name = 'accounts/user_list.html'
    table_class = tables.UserListTable
    model = auth.get_user_model()


# Admin Change/Edit User (modal)
class UserChange(UpdateView):
    """
    Change/Edit User view. Used in a modal window.
    """
    model = auth.get_user_model()
    success_url = reverse_lazy('accounts_user_list', args=())
    form_class = forms.UserChangeForm
    template_name = 'accounts/deployuser_change.html'

    def dispatch(self, request, *args, **kwargs):
        # Edit your profile or you're an admin, load the view
        if self.request.user.pk == int(kwargs.get('pk')) or self.request.user.user_is_admin():
            return super(UserChange, self).dispatch(request, *args, **kwargs)

        # Redirect to index or login for other users
        if request.user.is_authenticated():
            return redirect('index')
        else:
            return redirect_to_login(request.get_full_path())

    def get_form_kwargs(self):
        kwargs = super(UserChange, self).get_form_kwargs()
        kwargs['user_is_admin'] = self.request.user.user_is_admin()

        return kwargs


# Admin Add Users (modal)
class UserAdd(MultipleGroupRequiredMixin, CreateView):
    """
    Create User view. Used in a modal window.
    """
    group_required = 'Admin'
    model = auth.get_user_model()
    success_url = reverse_lazy('accounts_user_list', args=())
    form_class = forms.UserCreationForm
    template_name = 'accounts/deployuser_create.html'

    def get_form_kwargs(self):
        kwargs = super(UserAdd, self).get_form_kwargs()
        kwargs['user_is_admin'] = self.request.user.user_is_admin()

        return kwargs

    def form_valid(self, form):
        # Save form
        response = super(UserAdd, self).form_valid(form)

        # Send a password recover email
        email_form = PasswordResetForm({'email': form.cleaned_data['email']})
        email_form.is_valid()
        email_form.save(email_template_name='accounts/welcome_email.html')

        # send response
        return response


# Admin User Detail
class UserDetail(DetailView):
    model = auth.get_user_model()


# Admin Delete User
class UserDelete(MultipleGroupRequiredMixin, DeleteView):
    group_required = 'Admin'
    model = auth.get_user_model()
    success_url = reverse_lazy('accounts_user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User {} Successfully Deleted'.format(self.get_object()))
        return super(UserDelete, self).delete(self, request, *args, **kwargs)


class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'

    def get_success_url(self):
        return reverse('accounts_user_view', args=(self.request.user.id,))

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully')
        return super(PasswordChange, self).form_valid(form)
