# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Utilities for the tinkhan app.
"""
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils import timezone

from tincan_exporter.utils import StatementSource

from khan.models import Performance, BadgeEarn, Watch


def english(text):
    return {
        'en-US': text,
    }

def object_id(id):
    site = Site.objects.get_current()
    return 'http://' + site.domain + reverse('tincan_export_object_id', kwargs=dict(id=id))


def verbify(verb):
    """
    Output the verb definition
    """
    if type(verb) == type({}):
        return verb

    site = Site.objects.get_current()
    url = 'http://' + site.domain + reverse('tincan_export_verb', kwargs=dict(verb=verb))

    return dict(
        id=url,
        display=english(verb)
    )


def actor(person):
    """
    Output the TCAPI actor data for the person
    """
    actor = dict(
        objectType='Agent',
        name=person.name,
    )

    if person.use_tc_account:
        actor['account'] = dict(
            homePage=person.tc_account_homePage,
            id=person.tc_account_id,
        )
    elif person.openid:
        actor['openid'] = person.openid
    else:
        actor['mbox'] = 'mailto:' + person.email

    return actor


def statement(person, verb, **kwargs):
    statement = dict(
        actor=actor(person),
        verb=verbify(verb)
    )

    if 'timestamp' in kwargs:
        kwargs['timestamp'] = kwargs['timestamp'].strftime('%Y-%m-%dT%H:%M:%S%z')
    else:
        kwargs['timestamp'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S%z')

    statement.update(kwargs)
    return statement


class UserDataStatementSource(StatementSource):
    def __init__(self, userdata, person):
        assert person is not None
        assert person.userdata == userdata

        self.userdata = userdata
        self.person = person
        self._pending_statement_objects = []

    def _get_exercise_statements(self):
        statements = []
        for perf in Performance.objects.filter(synchronized=False, user=self.userdata):
            result = dict(
                completion=perf.proficient_date is not None,
                success=perf.first_done is not None
            )
            obj = dict(
                id=object_id(id='exercise'),
                definition=dict(
                    name=english(perf.exercise.name),
                    description=english(perf.exercise.description)
                )
            )
            statements.append(
                    statement(self.person, 'answered',
                        object=obj,
                        result=result,
                        timestamp=(perf.last_done or perf.first_done or timezone.now())
                    ))
            self._pending_statement_objects.append(perf)

        return statements

    def _get_video_statements(self):
        statements = []
        for watch in Watch.objects.filter(synchronized=False, user=self.userdata):
            result = dict(
                completion=watch.completed
            )
            obj = dict(
                id=object_id(id='video'),
                definition=dict(
                    name=english(watch.video.title),
                    description=english(watch.video.description)
                )
            )
            statements.append(
                    statement(self.person, 'viewed',
                        object=obj,
                        result=result,
                        timestamp=watch.last_watched
                    ))
            self._pending_statement_objects.append(watch)

        return statements

    def _get_badge_statements(self):
        statements = []
        for earn in BadgeEarn.objects.filter(synchronized=False, user=self.userdata):
            obj = dict(
                id=object_id(id='badge'),
                definition=dict(
                    name=english(earn.badge.name),
                    description=english(earn.badge.description)
                )
            )
            statements.append(
                    statement(self.person, 'earned',
                        object=obj,
                        timestamp=earn.date_earned
                    ))
            self._pending_statement_objects.append(earn)

        return statements

    def get(self):
        # what exercises did we attempt/complete?
        # what videos did we watch?
        # what badges did we earn?
        return self._get_exercise_statements() + \
               self._get_video_statements() + \
               self._get_badge_statements()

    def commit(self):
        # TODO some sort of bulk operation here...
        for obj in self._pending_statement_objects:
            obj.synchronize()
