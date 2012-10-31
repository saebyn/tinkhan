# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Views for the tinkhan app.
"""
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import DetailView, SingleObjectMixin

from oauth_hook import OAuthHook
from urlparse import parse_qs
import requests
from requests.exceptions import RequestException

from tinkhan_app.models import Person
from tinkhan_app.settings import OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET
from tinkhan_app.tasks import update_person


class HomeView(TemplateView):
    template_name = 'tinkhan_app/home.html'


home = HomeView.as_view()


class AuthorizeKhanImportView(SingleObjectMixin, RedirectView):
    """
    Redirect view for users that get emailed about authing us to pull their khan academy info.
    """
    permanent = False
    queryset = Person.objects.all()

    def get_redirect_url(self, **kwargs):
        self.object = self.get_object()

        # set up the initial request for a request token
        oauth_hook = OAuthHook(
            consumer_key=OAUTH_CONSUMER_KEY,
            consumer_secret=OAUTH_CONSUMER_SECRET
        )

        # generate the callback (return) url
        oauth_callback = self.request.build_absolute_uri(
                reverse('start_khan_import', kwargs=dict(pk=self.object.pk))
        )

        # make the request
        response = requests.post('https://www.khanacademy.org/api/auth/request_token',
            params={'oauth_callback': oauth_callback},
            headers={'Content-Length': '0'},
            hooks={'pre_request': oauth_hook},
            allow_redirects=False
        )
        return response.headers['location']


authorize_khan_import = AuthorizeKhanImportView.as_view()


class StartKhanImportView(SingleObjectMixin, RedirectView):
    """
    Redirect view for users returning from oauth at khan academy,
    where we start the import/export process.
    """
    permanent = False
    queryset = Person.objects.all()

    def get_redirect_url(self, **kwargs):
        self.object = self.get_object()

        try:
            # get final oauth tokens
            oauth_hook = OAuthHook(
                self.request.GET['oauth_token'],
                self.request.GET['oauth_token_secret'],
                consumer_key=OAUTH_CONSUMER_KEY,
                consumer_secret=OAUTH_CONSUMER_SECRET
            )

            response = requests.post(
                'https://www.khanacademy.org/api/auth/access_token',
                params={'oauth_verifier': self.request.GET['oauth_verifier']},
                headers={'Content-Length': '0'},
                hooks={'pre_request': oauth_hook})
            response.raise_for_status()

            # Extract final oauth token
            qs = parse_qs(response.text)
            oauth_token = qs['oauth_token'][0]
            oauth_secret = qs['oauth_token_secret'][0]
        except (KeyError, RequestException):
            return reverse('khan_import_auth_problem', kwargs=dict(pk=self.object.pk))

        # Build oauth hook for celery task to use
        final_oauth_hook = OAuthHook(
            oauth_token,
            oauth_secret,
            OAUTH_CONSUMER_KEY,
            OAUTH_CONSUMER_SECRET,
            True
        )

        # Start up the update process
        update_person.delay(final_oauth_hook, self.object)

        return reverse('started_khan_import', kwargs=dict(pk=self.object.pk))


start_khan_import = StartKhanImportView.as_view()


class StartedKhanImportView(DetailView):
    template_name = 'tinkhan_app/started_khan_import.html'
    queryset = Person.objects.all()
    context_object_name = 'person'


started_khan_import = StartedKhanImportView.as_view()


class KhanImportAuthProblemView(DetailView):
    template_name = 'tinkhan_app/import_auth_problem.html'
    queryset = Person.objects.all()
    context_object_name = 'person'


khan_import_auth_problem = KhanImportAuthProblemView.as_view()


# interface for account holder to:
#  - configure their tcapi endpoints
#  - manage their people
#  - send the emails
