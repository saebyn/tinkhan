# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Models for the tinkhan app.
"""

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from tincan_exporter.models import TinCanEndpoint

from khan.models import UserData


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tcapi_endpoint = models.OneToOneField(TinCanEndpoint, null=True, blank=True)
    company = models.CharField(max_length=100, default='', blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.company, self.user.get_full_name())


class Person(models.Model):
    account = models.ForeignKey(UserProfile)
    userdata = models.ForeignKey(UserData, null=True, blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    openid = models.URLField(blank=True)

    use_tc_account = models.BooleanField(default=False)
    tc_account_homePage = models.CharField(max_length=255, blank=True)
    tc_account_id = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.account.company)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile(user=user)
        profile.save()


post_save.connect(create_profile, sender=User,
        dispatch_uid="users-profilecreation-signal")
