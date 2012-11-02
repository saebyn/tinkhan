# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Celery tasks for the tinkhan app.
"""
from django.template import Context, loader
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail

import celery
from celery.utils.log import get_task_logger

from khan.tasks import fetch_user
from tincan_exporter.tasks import export_statements

from tinkhan_app.utils import UserDataStatementSource


logger = get_task_logger(__name__)


@celery.task(ignore_result=True)
def send_email_request_for_userdata_update_for_account(account_profile):
    # for each person managed by this account profile, send the email requesting oauth
    # access to their khan academy information
    emails = []

    for person in account_profile.person_set.all():
        # 1. render text context to email template
        email_template = loader.get_template('tinkhan_app/email/auth_request.txt')
        site = Site.objects.get_current()
        context = Context({'person': person,
                           'site': site})
        email_contents = email_template.render(context)
        subject = _('Update %s with your latest work from Khan Academy via %s')
        emails.append((subject % (account_profile.company, site.name,),
                       email_contents,
                       settings.FROM_EMAIL,
                       [person.email]))

    # 2. send emails
    send_mass_mail(emails)


@celery.task(ignore_result=True)
def update_person_userdata(userdata, person):
    person.userdata = userdata
    person.save()
    return userdata


@celery.task(ignore_result=True)
def export_persons_statements(userdata, person):
    if person.account.tcapi_endpoint is not None:
        export_statements([UserDataStatementSource(userdata, person)], person.account.tcapi_endpoint)


@celery.task(ignore_result=True)
def update_person(oauth_hook, person):
    # given that we have an oauth token (via oauth_hook)
    # - use khan.tasks.fetch_user
    # - use the userdata instance it returns to ensure that the person instance
    #   if associated with it
    # - wrap the userdata instance in our implementation of StatementSource
    #   and send that to the tincan_exporter.tasks.export_statements task
    (fetch_user.s(oauth_hook) | update_person_userdata.s(person) | export_persons_statements.s(person)).apply_async()
