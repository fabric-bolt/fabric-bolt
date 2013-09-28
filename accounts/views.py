"""
Deployment User Views
"""

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView, UpdateView, CreateView

from django_tables2 import RequestConfig
from django_filters.views import FilterView
from braces.views import GroupRequiredMixin

from . import forms


class Login(TemplateView):
    """
    Login view handles generating the login form, login authentication, and redirect after auth
    """
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        return {'form': forms.LoginForm}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(email=email, password=password)

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
class UserList(GroupRequiredMixin, FilterView):
    """
    List of users. Uses UserFilter and UserTable.
    """
    group_required = 'Admin'
    template_name_suffix = '_list'
    filterset_class = filters.UserFilter
    table_class = tables.UserListTable

    def get_queryset(self):
        users = auth.get_user_model()
        return users.objects.filter(is_staff=False)

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        table = self.table_class(kwargs['object_list'])
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context['table'] = table
        return context


# Admin Change/Edit User (modal)
class UserChange(GroupRequiredMixin, UpdateView):
    """
    Change/Edit User view. Used in a modal window.
    """
    group_required = 'Admin'
    model = auth.get_user_model()
    success_url = reverse_lazy('accounts_user_list', args=())
    form_class = forms.UserChangeForm


# Admin Add Users (modal)
class UserAdd(GroupRequiredMixin, CreateView):
    """
    Create User view. Used in a modal window.
    """
    group_required = 'Admin'
    model = auth.get_user_model()
    success_url = reverse_lazy('accounts_user_list', args=())
    form_class = forms.AtheneUserCreationForm

    def form_valid(self, form):
        response = super(UserAdd, self).form_valid(form)

        # Send a password recover email
        form = PasswordResetForm({'email': form.cleaned_data['email']})
        form.save(email_template_name='accounts/welcome_email.html')

        return response


# Admin Delete User
class UserDelete(GroupRequiredMixin, RedirectView):
    """
    Deletes a user from the system.
    """
    group_required = 'Admin'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = auth.get_user_model().objects.get(pk=pk)
        user.delete()

        messages.info(request, 'User %s was deleted successfully.' % user.email)
        return HttpResponseRedirect(reverse('athene_user_list'))
