# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Models for Tin Can APIs.
"""

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

import urlparse


class TinCanEndpoint(models.Model):
    BASIC_AUTH = 'b'
    AUTH_TYPES = (
        (BASIC_AUTH, 'HTTP Basic Authentication',),
    )

    auth_type = models.CharField(choices=AUTH_TYPES, max_length=1, default=BASIC_AUTH)
    username = models.CharField(max_length=255, blank=True, default='')
    password = models.CharField(max_length=255, blank=True, default='')
    hostname = models.CharField(max_length=255)
    ssl = models.BooleanField(default=True, verbose_name=_(u'SSL (https)'))
    path = models.CharField(max_length=255, default='/TCAPI/statements')
    user = models.ForeignKey(User, related_name='tincan_endpoints')

    def __unicode__(self):
        if self.username or self.hostname:
            return u'{0}@{1}'.format(self.username, self.hostname)
        else:
            return _(u'Unconfigured Endpoint')

    @property
    def url(self):
        parts = ['http', self.hostname, self.path, '', '', '']

        if self.ssl:
            parts[0] = 'https'

        return urlparse.urlunparse(parts)
