from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    url(r'^login/$', views.Login.as_view(), name='accounts_user_login'),
    url(r'^logout/$', views.Logout.as_view(), name='accounts_user_logout'),

    (r'^password_change/$',
    'django.contrib.auth.views.password_change',
    {'template_name': 'accounts/password_change_form.html'}),

    (r'^password_change/done/$',
    'django.contrib.auth.views.password_change_done',
    {'template_name': 'accounts/password_change_done.html'}),

    (r'^password_reset/$',
    'django.contrib.auth.views.password_reset',
    {'template_name': 'accounts/password_reset_form.html',
     'email_template_name': 'accounts/password_reset_email.html'}),

    (r'^password_reset/done/$',
    'django.contrib.auth.views.password_reset_done',
    {'template_name': 'accounts/password_reset_done.html'}),

    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    'django.contrib.auth.views.password_reset_confirm',
    {'template_name': 'accounts/password_reset_confirm.html'}),

    (r'^reset/done/$',
    'django.contrib.auth.views.password_reset_complete',
    {'template_name': 'accounts/password_reset_complete.html'}),
)

