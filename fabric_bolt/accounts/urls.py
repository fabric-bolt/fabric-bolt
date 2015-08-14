from django.conf.urls import url, include

from fabric_bolt.accounts import views

urlpatterns = [

    url(r'^$', views.UserList.as_view(), name='accounts_user_list'),
    url(r'^(?P<pk>.+)/$', views.UserDetail.as_view(), name='accounts_user_view'),
    url(r'^(?P<pk>.+)/update/$', views.UserChange.as_view(), name='accounts_user_change'),
    url(r'^(?P<pk>.+)/delete/$', views.UserDelete.as_view(), name='accounts_user_delete'),

    url(r'^add/$', views.UserAdd.as_view(), name='accounts_user_add'),
    url(r'^permissions/$', views.UserPermissions.as_view(), name='accounts_user_permissions'),

    url(r'^password_change/$', views.PasswordChange.as_view(), name='password_change'),
    url(r'^logout/$', 'authtools.views.logout_then_login', name='logout'),

    url(r'^', include('authtools.urls'))
]
