# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.conf.urls import patterns, url


urlpatterns = patterns('tincan_exporter.views',
    url(r'^verb/(?P<verb>\w+)/$',
        'verb',
        name='tincan_export_verb'),
    url(r'^object/(?P<id>\w+)/$',
        'object_id',
        name='tincan_export_object_id'),
)
