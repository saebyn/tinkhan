# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Forms for the tinkhan app.
"""
from django import forms

from django.utils.translation import ugettext_lazy as _

from html5forms.fields import Html5EmailField, Html5URLField, Html5CharField,\
        Html5BooleanField

from tinkhan_app.models import Person


# label openid, and the "tc" fields
# add help text for all fields
class PersonForm(forms.ModelForm):
    email = Html5EmailField()
    name = Html5CharField()
    openid = Html5URLField(required=False, help_text=_(u'''
The URI of an OpenID that uniquely identifies this user. If you provide this,
we'll use this instead of the email address when generating Tin Can API
statements.'''))

    use_tc_account = Html5BooleanField(label=_(u'Use account details'),
        required=False,
        help_text=_(u'''
If this is enabled, we'll use the user's account details you provide below to
uniquely identify this user when generating Tin Can API statements.'''))

    tc_account_homePage = Html5URLField(required=False,
        label=_(u'Account "homePage"'),
        help_text=_(u'''
The URI to the canonical home page for the system the account is on. This is based on FOAF's
accountServiceHomePage.'''))

    tc_account_id = Html5CharField(required=False, label=_(u'Account "name"'),
        help_text=_(u'''
The unique ID or name used to log in to this account. This is based on FOAF's
accountName.'''))

    class Meta:
        exclude = ('account', 'userdata',)
        model = Person

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PersonForm, self).__init__(*args, **kwargs)
        self.instance.account = user.get_profile()


# need modelform for endpoint?
