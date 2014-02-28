"""
Deployment User Views
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import password_reset_confirm, redirect_to_login
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView, UpdateView, CreateView, DeleteView, DetailView
from django_tables2 import SingleTableView

from fabric_bolt.core.mixins.views import MultipleGroupRequiredMixin
from fabric_bolt.accounts import forms, tables


class UserPermissions(TemplateView):
    template_name = 'accounts/permissions.html'


class Login(TemplateView):
    """
    Login view handles generating the login form, login authentication, and redirect after auth
    """

    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        return {'form': forms.LoginForm}

    def get(self, request, *args, **kwargs):
        """If the user is authenticated take them to the homepage"""

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Verify the correct username and password have been set and let them in if so
        """

        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(email=email, password=password)

        # Log the user in and send them on their merry way
        if user is not None and user.is_active:
            auth.login(request, user)
            goto = request.GET.get('next', reverse('index'))
            return HttpResponseRedirect(goto)

        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return HttpResponseRedirect(reverse('accounts_user_login'))


class Logout(TemplateView):
    """
    Logout view calls logout() on the request and redirects to the login screen
    """

    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts_user_login'))

        auth.logout(request)

        return HttpResponseRedirect(reverse('accounts_user_login'))


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


class PasswordChange(FormView):

    template_name = 'accounts/password_change.html'

    def get_success_url(self):
        return reverse('accounts_user_view', args=(self.request.user.id,))

    def get_form(self, form_class):
        return forms.UserPasswordChangeForm(self.request.user, self.request.POST or None)

    def form_valid(self, form):
        form.save()
        return super(PasswordChange, self).form_valid(form)


class PasswordCreate(FormView):

    template_name = 'accounts/password_create.html'

    def get_success_url(self):
        return reverse('accounts_user_view', args=(self.request.user.id,))

    def get_form(self, form_class):
        return forms.UserPasswordCreateForm(self.request.user, self.request.POST or None)

    def post(self, request, *args, **kwargs):
        return password_reset_confirm(request, **kwargs)
