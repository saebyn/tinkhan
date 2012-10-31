# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Settings for the tinkhan app.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
    OAUTH_CONSUMER_KEY = getattr(settings, 'TINKHAN_OAUTH_CONSUMER_KEY')
except AttributeError:
    raise ImproperlyConfigured('The TINKHAN_OAUTH_CONSUMER_KEY must be set to the consumer key provided by Khan Academy for this app.')

try:
    OAUTH_CONSUMER_SECRET = getattr(settings, 'TINKHAN_OAUTH_CONSUMER_SECRET')
except AttributeError:
    raise ImproperlyConfigured('The TINKHAN_OAUTH_CONSUMER_SECRET must be set to the consumer secret provided by Khan Academy for this app.')
