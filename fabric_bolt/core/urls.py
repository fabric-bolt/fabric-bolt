from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from fabric_bolt.core import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Dashboard.as_view(), name='index'),
    url(r'^hosts/', include('fabric_bolt.hosts.urls')),
    url(r'^web-hooks/', include('fabric_bolt.web_hooks.urls')),
    url(r'^launch-window/', include('fabric_bolt.launch_window.urls')),
    url(r'^projects/', include('fabric_bolt.projects.urls')),
    url(r'^users/', include('fabric_bolt.accounts.urls')),
]

# Serve the static files from django

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
