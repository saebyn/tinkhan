# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Celery tasks for Tin Can Statement export.
"""
import celery
from celery.utils.log import get_task_logger

import requests
import requests.exceptions

import json

from tincan_exporter.models import TinCanEndpoint

logger = get_task_logger(__name__)


@celery.task(ignore_result=True)
def export_statements(statement_sources, tcapi_endpoint):
    """
    Get the statements from each source in statement_sources and send
    to the tcapi_endpoint.
    """
    logger.info('Exporting Tin Can statements')

    statements = []

    for source in statement_sources:
        statements.extend(source.get())

    request_options = {
        'headers': {
            'content-type': 'application/json',
            'x-experience-api-version': '0.95',
        },
    }

    if tcapi_endpoint.auth_type == TinCanEndpoint.BASIC_AUTH:
        request_options['auth'] = (tcapi_endpoint.username, tcapi_endpoint.password)
    else:
        logger.warning('Unknown auth_type for tcapi_endpoint: %s' % tcapi_endpoint.get_auth_type_display())

    request_options['data'] = json.dumps(statements)

    try:
        requests.post(tcapi_endpoint.url, **request_options)
    except requests.exceptions.RequestException, exc:
        raise export_statements.retry(exc=exc)

    for source in statement_sources:
        source.commit()

    logger.info('Finished exporting Tin Can statements')
