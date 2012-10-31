# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Models for the tinkhan app.
"""

from django.db import models

from django.contrib.auth.models import User

from tincan_exporter.models import TinCanEndpoint

from khan.models import UserData


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tcapi_endpoint = models.OneToOneField(TinCanEndpoint)
    company = models.CharField(max_length=100)


class Person(models.Model):
    account = models.ForeignKey(UserProfile)
    userdata = models.ForeignKey(UserData)
    email = models.EmailField()
    name = models.CharField(max_length=255)

    use_tc_account = models.BooleanField(default=False)
    tc_account_homePage = models.CharField(max_length=255, blank=True)
    tc_account_id = models.CharField(max_length=255, blank=True)
