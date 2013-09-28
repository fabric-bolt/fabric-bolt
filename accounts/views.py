"""
Deployment User Views
"""

from django.contrib import auth
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

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