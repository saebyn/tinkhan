# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': (),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tinkhan.views.home', name='home'),

    url(r'', include('tinkhan_app.urls')),

    # generic and contrib views
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^accounts/profile/', include('profiles.urls')),
    url(r'^accounts/', include('registration.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)


# terms of service links
urlpatterns += patterns('',
    (r'^login/$', 'tos.views.login', {}, 'login',),
    (r'^terms-of-service/', include('tos.urls')),
)
