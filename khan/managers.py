# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Model managers for the `khan` Django app.
"""
import logging

from django.db import models
from django.utils import timezone


logger = logging.getLogger(__name__)


class ExerciseManager(models.Manager):
    def load(self, data, user):
        """
        Load the UserData.exercise_performances m2m.
        """
        from khan.models import Performance

        performances = []

        for performance_data in data:
            assert performance_data['kind'] == 'UserExercise'

            try:
                exercise = self.get(khan_id=performance_data['exercise'])
            except self.model.DoesNotExist:
                logger.warning('Failed to find exercise "%(exercise)s" for performance for "%(user)s"' % performance_data)
                continue

            try:
                performance = Performance.objects.get(user=user, exercise=exercise)
            except Performance.DoesNotExist:
                performance = Performance(user=user, exercise=exercise)

            performance.first_done = performance_data.get('first_done', None) or None
            performance.last_done = performance_data.get('last_done', None) or None
            performance.last_review = performance_data.get('last_review', None) or None
            performance.proficient_date = performance_data.get('proficient_date', None) or None

            performance.longest_streak = performance_data.get('longest_streak', 0) or 0
            performance.streak = performance_data.get('streak', 0) or 0
            performance.total_done = performance_data.get('total_done', 0) or 0
            performance.summative = performance_data.get('summative', False) or False
            performance.seconds_per_fast_problem = performance_data.get('seconds_per_fast_problem', 0) or 0
            performance.save()

            performances.append(performance)

        return performances


class VideoManager(models.Manager):
    def load(self, data, user):
        """
        Load the UserData.watched_videos m2m.
        """
        from khan.models import Watch

        watched = []

        for watch_data in data:
            assert watch_data['kind'] == 'UserVideo'

            video, created = self.get_or_create(
                khan_id=watch_data['video']['readable_id'],
                defaults=dict(
                    title=watch_data['video']['title'],
                    description=watch_data['video']['description'],
                    duration=watch_data['video']['duration'],
                    url=watch_data['video']['ka_url'],
                    youtube_id=watch_data['video']['youtube_id'],
                    views=watch_data['video']['views'],
                    date_added=watch_data['video']['date_added'],
                ))

            try:
                watch = Watch.objects.get(user=user, video=video)
            except Watch.DoesNotExist:
                watch = Watch(user=user, video=video)

            watch.completed = watch_data['completed']
            watch.last_second_watched = watch_data['last_second_watched']
            watch.last_watched = watch_data['last_watched']
            watch.points = watch_data['points']
            watch.seconds_watched = watch_data['seconds_watched']
            watch.save()

            watched.append(watch)

        return watched


class BadgeManager(models.Manager):
    def load(self, categories_data, data, user):
        """
        Load badges, badge categories, and the UserData.earned_badges m2m.
        """
        from khan.models import BadgeCategory, BadgeEarn, Exercise

        for category_data in categories_data:
            try:
                category = BadgeCategory.objects.get(khan_id=category_data['category'])
            except BadgeCategory.DoesNotExist:
                category = BadgeCategory(khan_id=category_data['category'])

            category.description = category_data['description']
            category.type_label = category_data['type_label']
            category.chart_icon_src = category_data['chart_icon_src']
            category.icon_src = category_data['icon_src']
            category.large_icon_src = category_data['large_icon_src']
            category.save()

        badges = []

        for badge_data in data:
            try:
                badge = self.get(khan_id=badge_data['name'])
            except self.model.DoesNotExist:
                badge = self.model(khan_id=badge_data['name'])

            badge.category = BadgeCategory.objects.get(khan_id=badge_data['badge_category'])
            badge.name = badge_data['description']
            badge.description = badge_data['safe_extended_description']
            badge.points = badge_data['points']
            badge.save()

            badges.append(badge)

            new_badges = []

            existing_badges = BadgeEarn.objects.filter(user=user, badge=badge)\
                    .values_list('badge__khan_id', 'date_earned')

            for user_badge in badge_data.get('user_badges', []):
                assert user_badge['kind'] == 'UserBadge'
                assert user_badge['badge_name'] == badge.khan_id
                if (user_badge['badge_name'], user_badge['date']) not in existing_badges:
                    badge_earn = BadgeEarn(
                        user=user,
                        badge=badge,
                        date_earned=(user_badge.get('date', None) or timezone.now()),
                        points_earned=(user_badge.get('points_earned', 0) or 0),
                        target_context_name=(user_badge.get('target_context_name', '') or '')
                    )

                    try:
                        if user_badge['target_context']['kind'] == 'Exercise':
                            try:
                                badge_earn.target_context = Exercise.objects.get(khan_id=user_badge['target_context']['name'])
                            except Exercise.DoesNotExist:
                                logger.warning('Failed to find exercise for badge "%(badge_name)s" for user "%(user)s"' % user_badge)
                    except (KeyError, TypeError):
                        pass

                    new_badges.append(badge_earn)

            BadgeEarn.objects.bulk_create(new_badges)

        return badges


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

        # this code and the similar pair elsewhere in the file needs to be refactored
        present = frozenset(x[0] for x in obj.proficient_exercises.values_list('khan_id'))
        correct = frozenset(proficient_exercises)
        absent = correct - present
        extra = present - correct

        for exercise in extra:
            obj.proficient_exercises.remove(Exercise.objects.get(khan_id=exercise))

        for exercise in absent:
            try:
                obj.proficient_exercises.add(Exercise.objects.get(khan_id=exercise))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for proficient exercises while adding "%s"' % (exercise, data['user_id']))

        present = frozenset(x[0] for x in obj.suggested_exercises.values_list('khan_id'))
        correct = frozenset(suggested_exercises)
        absent = correct - present
        extra = present - correct

        for exercise in extra:
            obj.suggested_exercises.remove(Exercise.objects.get(khan_id=exercise))

        for exercise in absent:
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

        current_prereqs = frozenset(x[0] for x in obj.prerequisites.all().values_list('khan_id'))
        needed_prereqs = frozenset(prerequisites)
        no_longer_prereqs = current_prereqs - needed_prereqs
        missing_prereqs = needed_prereqs - current_prereqs

        for prereq in obj.prerequisites.filter(khan_id__in=no_longer_prereqs):
            obj.prerequisites.remove(prereq)

        for prereq in missing_prereqs:
            try:
                obj.prerequisites.add(Exercise.objects.get(khan_id=prereq))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for prereq. while adding "%s"' % (prereq, obj.name))

        current_covers = frozenset(x[0] for x in obj.covers.all().values_list('khan_id'))
        needed_covers = frozenset(covers)
        no_longer_covers = current_covers - needed_covers
        missing_covers = needed_covers - current_covers

        for cover in obj.covers.filter(khan_id__in=no_longer_covers):
            obj.covers.remove(cover)

        for cover in missing_covers:
            try:
                obj.covers.add(Exercise.objects.get(khan_id=cover))
            except Exercise.DoesNotExist:
                logger.warning('Failed to find exercise "%s" for cover while adding "%s"' % (cover, obj.name))

        return obj
