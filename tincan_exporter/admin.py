# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.contrib import admin

from tincan_exporter.models import TinCanEndpoint


admin.site.register(TinCanEndpoint)
