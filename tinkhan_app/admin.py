# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.contrib import admin

from tinkhan_app.models import UserProfile, Person


admin.site.register(UserProfile)
admin.site.register(Person)
