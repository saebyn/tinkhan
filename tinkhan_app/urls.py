# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.conf.urls import patterns, url


urlpatterns = patterns('tinkhan_app.views',
    url(r'^$', 'home', name='home'),

    url(r'^import/(?P<pk>\d+)/$',
        'authorize_khan_import',
        name='authorize_khan_import'),

    url(r'^import/(?P<pk>\d+)/start/$',
        'start_khan_import',
        name='start_khan_import'),

    url(r'^import/(?P<pk>\d+)/started/$',
        'started_khan_import',
        name='started_khan_import'),
)
