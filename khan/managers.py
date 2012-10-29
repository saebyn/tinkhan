# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Model managers for the `khan` Django app.
"""
import logging

from django.db import models


logger = logging.getLogger(__name__)


class ExerciseManager(models.Manager):
    def load(self, data, user):
        """
        Load the UserData.exercise_performances m2m.
        """
        # TODO
        obj = None
        return obj


class VideoManager(models.Manager):
    def load(self, data, user):
        """
        Load the UserData.watched_videos m2m.
        """
        # TODO
        obj = None
        return obj


class BadgeManager(models.Manager):
    def load(self, data, user):
        """
        Load badges, badge categories, and the UserData.earned_badges m2m.
        """
        # TODO
        obj = None
        return obj


class UserDataManager(models.Manager):
    def load(self, data):
        from khan.models import Exercise
        assert data['kind'] == 'UserData'

        nickname = data.get('nickname', '') or ''
        prettified_user_email = data.get('prettified_user_email', '') or ''
        joined = data.get('joined', None)
        last_activity = data.get('last_activity', None)
        points = data.get('points', 0) or 0
        proficient_exercises = data.get('proficient_exercises', []) or []
        suggested_exercises = data.get('suggested_exercises', []) or []
        total_seconds_watched = data.get('total_seconds_watched', 0) or 0

        obj, created = self.get_or_create(
                user_id=data['user_id'],
                defaults=dict(
                    nickname=nickname,
                    prettified_user_email=prettified_user_email,
                    joined=joined,
                    last_activity=last_activity,
                    points=points,
                    total_seconds_watched=total_seconds_watched))

        if not created:
            obj.nickname = nickname
            obj.prettified_user_email = prettified_user_email
            obj.joined = joined
            obj.last_activity = last_activity
            obj.total_seconds_watched = total_seconds_watched
            obj.save()

        obj.proficient_exercises.all().delete()
        for exercise in proficient_exercises:
            try:
                obj.proficient_exercises.add(Exercise.objects.get(khan_id=exercise))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for proficient exercises while adding "%s"' % (exercise, data['user_id']))

        obj.suggested_exercises.all().delete()
        for exercise in suggested_exercises:
            try:
                obj.suggested_exercises.add(Exercise.objects.get(khan_id=exercise))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for suggested exercises while adding "%s"' % (exercise, data['user_id']))

        return obj


class TopicManager(models.Manager):
    def load(self, data, parent=None):
        assert data['kind'] == 'Topic'

        title = data.get('title', '') or ''
        description = data.get('description', '') or ''
        url = data.get('ka_url', '') or ''
        children = data.get('children', []) or []

        obj, created = self.get_or_create(
                khan_id=data['id'],
                defaults=dict(
                    title=title,
                    description=description,
                    url=url,
                    parent=parent))
        if not created:
            obj.title = title
            obj.description = description
            obj.url = url
            obj.parent = parent
            obj.save()

        for child in children:
            if child['kind'] == 'Topic':
                self.load(child, obj)
            elif child['kind'] == 'Video':
                self.load_video(child, obj)
            elif child['kind'] == 'Exercise':
                self.load_exercise(child, obj)

        return obj

    def load_video(self, data, topic):
        from khan.models import Video
        assert data['kind'] == 'Video'

        title = data.get('title', '') or ''
        description = data.get('description', '') or ''
        position = data.get('position', 0) or 0
        keywords = data.get('keywords', '') or ''
        duration = data.get('duration', 0) or 0
        url = data.get('ka_url', '') or ''
        youtube_id = data.get('youtube_id', '') or ''
        views = data.get('views', 0) or 0
        date_added = data.get('date_added', None)

        obj, created = Video.objects.get_or_create(
                khan_id=data['readable_id'],
                defaults=dict(
                    title=title,
                    description=description,
                    keywords=keywords,
                    position=position,
                    duration=duration,
                    url=url,
                    youtube_id=youtube_id,
                    views=views,
                    date_added=date_added,
                    topic=topic
                ))

        if not created:
            obj.title = title
            obj.description = description
            obj.keywords = keywords
            obj.position = position
            obj.duration = duration
            obj.url = url
            obj.youtube_id = youtube_id
            obj.views = views
            obj.date_added = date_added
            obj.topic = topic
            obj.save()

        return obj

    def load_exercise(self, data, topic):
        from khan.models import Exercise

        assert data['kind'] == 'Exercise'

        name = data.get('display_name', '') or ''
        short_name = data.get('short_display_name', '') or ''
        description = data.get('description', '') or ''
        live = data.get('live', False) or False
        summative = data.get('summative', False) or False
        url = data.get('ka_url', '') or ''
        prerequisites = data.get('prerequisites', []) or []
        covers = data.get('covers', []) or []
        h_position = data.get('h_position', 0) or 0
        v_position = data.get('v_position', 0) or 0
        seconds_per_fast_problem = data.get('seconds_per_fast_problem', 0) or 0

        obj, created = Exercise.objects.get_or_create(
                khan_id=data['name'],
                defaults=dict(
                    name=name,
                    short_name=short_name,
                    description=description,
                    live=live,
                    summative=summative,
                    url=url,
                    h_position=h_position,
                    v_position=v_position,
                    seconds_per_fast_problem=seconds_per_fast_problem,
                    topic=topic
                ))

        if not created:
            obj.name = name
            obj.description = description
            obj.live = live
            obj.summative = summative
            obj.url = url
            obj.h_position = h_position
            obj.v_position = v_position
            obj.seconds_per_fast_problem = seconds_per_fast_problem
            obj.topic = topic
            obj.save()

        obj.prerequisites.all().delete()
        for prerequisite in prerequisites:
            try:
                obj.prerequisites.add(Exercise.objects.get(khan_id=prerequisite))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for prereq. while adding "%s"' % (prerequisite, data['name']))

        obj.covers.all().delete()
        for cover in covers:
            try:
                obj.covers.add(Exercise.objects.get(khan_id=cover))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for cover while adding "%s"' % (prerequisite, data['name']))

        return obj
