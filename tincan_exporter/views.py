# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.views.generic import TemplateView


class ObjectIdView(TemplateView):
    template_name = 'tincan_exporter/object_id.html'


object_id = ObjectIdView.as_view()


class VerbView(TemplateView):
    template_name = 'tincan_exporter/verb.html'


verb = VerbView.as_view()
