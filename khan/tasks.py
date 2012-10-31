# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Celery tasks for the `khan` Django app.
"""
import requests
import requests.exceptions

import celery
from celery.utils.log import get_task_logger

from khan.models import Topic, UserData, Exercise, Video, Badge

logger = get_task_logger(__name__)


@celery.task(ignore_result=True, rate_limit='1/h')
def update_topic_tree():
    logger.info('Updating topic tree')
    try:
        response = requests.get('http://www.khanacademy.org/api/v1/topictree')
    except requests.exceptions.RequestException, exc:
        raise update_topic_tree.retry(exc=exc)
    
    topic_tree = response.json
    if topic_tree is None:
        raise update_topic_tree.retry()

    Topic.objects.load(topic_tree)

    logger.info('Finished updating topic tree')


@celery.task(ignore_result=True, rate_limit='1/h')
def update_badge_categories():
    logger.info('Updating badge categories')
    try:
        response = requests.get('http://www.khanacademy.org/api/v1/badges/categories')
    except requests.exceptions.RequestException, exc:
        raise update_badge_categories.retry(exc=exc)
    
    categories = response.json
    if categories is None:
        raise update_badge_categories.retry()

    Badge.objects.load(categories, [], None)

    logger.info('Finished updating badge categories')


@celery.task(rate_limit='6/h')
def fetch_user(oauth_hook):
    logger.info('Fetch all user-specific data')
    
    fetch_workflow = (fetch_userdata.s(oauth_hook) | celery.group([
        fetch_user_exercises.s(oauth_hook),
        fetch_user_videos.s(oauth_hook),
        fetch_user_badges.s(oauth_hook),
    ]))()

    logger.info('Finished fetching all user-specific data')

    return fetch_workflow.parent.get()  # return the userdata instance


@celery.task(rate_limit='6/h')
def fetch_userdata(oauth_hook):
    logger.info('Fetching userdata')

    try:
        response = requests.get('http://www.khanacademy.org/api/v1/user',
                hooks=dict(pre_request=oauth_hook))

        if response.status_code == 401:
            return None
    except requests.exceptions.RequestException, exc:
        raise fetch_userdata.retry(exc=exc)

    raw_userdata = response.json
    if raw_userdata is None:
        raise fetch_userdata.retry()

    userdata = UserData.objects.load(raw_userdata)

    logger.info('Finished fetching userdata')

    return userdata


@celery.task(rate_limit='6/h')
def fetch_user_exercises(userdata, oauth_hook):
    logger.info('Fetching user exercise data')

    try:
        response = requests.get('http://www.khanacademy.org/api/v1/user/exercises',
                hooks=dict(pre_request=oauth_hook))

        if response.status_code == 401:
            return False
    except requests.exceptions.RequestException, exc:
        raise fetch_user_exercises.retry(exc=exc)

    raw_data = response.json
    if raw_data is None:
        raise fetch_user_exercises.retry()

    count = len(Exercise.objects.load(raw_data, userdata))

    logger.info('Finished fetching user exercise data')

    return count


@celery.task(rate_limit='6/h')
def fetch_user_videos(userdata, oauth_hook):
    logger.info('Fetching user video data')

    try:
        response = requests.get('http://www.khanacademy.org/api/v1/user/videos',
                hooks=dict(pre_request=oauth_hook))

        if response.status_code == 401:
            return False
    except requests.exceptions.RequestException, exc:
        raise fetch_user_videos.retry(exc=exc)

    raw_data = response.json
    if raw_data is None:
        raise fetch_user_videos.retry()

    count = len(Video.objects.load(raw_data, userdata))

    logger.info('Finished fetching user video data')

    return count


@celery.task(rate_limit='6/h')
def fetch_user_badges(userdata, oauth_hook):
    logger.info('Fetching user badge data')

    try:
        response = requests.get('http://www.khanacademy.org/api/v1/badges',
                hooks=dict(pre_request=oauth_hook))

        if response.status_code == 401:
            return False
    except requests.exceptions.RequestException, exc:
        raise fetch_user_badges.retry(exc=exc)

    raw_data = response.json
    if raw_data is None:
        raise fetch_user_badges.retry()

    count = len(Badge.objects.load([], raw_data, userdata))

    logger.info('Finished fetching user badge data')

    return count
