from django.conf.urls import url, patterns

from fabric_bolt.accounts import views

urlpatterns = patterns('',
    url(r'^login/$', views.Login.as_view(), name='accounts_user_login'),
    url(r'^logout/$', views.Logout.as_view(), name='accounts_user_logout'),
    url(r'^users/$', views.UserList.as_view(), name='accounts_user_list'),
    url(r'^user/add/$', views.UserAdd.as_view(), name='accounts_user_add'),
    url(r'^user/change/(?P<pk>.+)/$', views.UserChange.as_view(), name='accounts_user_change'),
    url(r'^user/view/(?P<pk>.+)/$', views.UserDetail.as_view(), name='accounts_user_view'),
    url(r'^user/delete/(?P<pk>.+)/$', views.UserDelete.as_view(), name='accounts_user_delete'),
    url(r'^password_change/$', views.PasswordChange.as_view(), name='accounts_password_change'),  # django.contrib.auth.views.password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordCreate.as_view(), name='auth_password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)