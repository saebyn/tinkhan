# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Unit tests for the `khan` Django app.
"""

import json

from django.test import TestCase

from django.utils import timezone


class DataLoadTest(TestCase):
    def test_load_badges(self):
        from khan.models import UserData, Badge, Exercise, BadgeEarn

        user = UserData.objects.create(
            nickname='test',
            user_id='you@gmail.com',
            prettified_user_email='',
            joined=timezone.now(),
            last_activity=timezone.now(),
            points=0,
            total_seconds_watched=0
        )

        Exercise.objects.create(
            name='',
            short_name='',
            description='',
            live=False,
            summative=False,
            khan_id='addition_1',
            url='',
            h_position=0,
            v_position=0,
            seconds_per_fast_problem=0
        )

        # /api/v1/badges/categories

        categories_data = """
[
    {
        "category": 0, 
        "chart_icon_src": "/images/badges/meteorite-small-chart.png", 
        "description": "Meteorite badges are common and easy to earn when just getting started.", 
        "icon_src": "/images/badges/meteorite-small.png", 
        "large_icon_src": "/images/badges/meteorite.png", 
        "type_label": "Meteorite"
    }, 
    {
        "category": 1, 
        "chart_icon_src": "/images/badges/moon-small-chart.png", 
        "description": "Moon badges are uncommon and represent an investment in learning.", 
        "icon_src": "/images/badges/moon-small.png", 
        "large_icon_src": "/images/badges/moon.png", 
        "type_label": "Moon"
    }
]
        """

        # /api/v1/badges

        badges_data = """
[
    {
        "badge_category": 1, 
        "description": "Going Transonic", 
        "name": "greattimedproblembadge", 
        "points": 500, 
        "safe_extended_description": "Quickly & correctly answer 10 exercise problems in a row (time limit depends on exercise difficulty)", 
        "user_badges": [
            {
                "badge_name": "greattimedproblembadge", 
                "date": "2011-05-04T06:02:05Z", 
                "kind": "UserBadge", 
                "points_earned": 500, 
                "target_context": {
                    "kind": "Exercise",
                    "name": "addition_1"
                }, 
                "target_context_name": "Addition 1", 
                "user": "you@gmail.com"
            }
        ]
    }
]
        """

        badge = Badge.objects.load(
                json.loads(categories_data),
                json.loads(badges_data)
                , user)[0]

        self.assertEqual(
                BadgeEarn.objects.get(badge=badge, user=user).target_context,
                Exercise.objects.get(khan_id='addition_1')
        )


    def test_load_video_watch(self):
        from khan.models import Video, UserData, Watch

        user = UserData.objects.create(
            nickname='test',
            user_id='you@gmail.com',
            prettified_user_email='',
            joined=timezone.now(),
            last_activity=timezone.now(),
            points=0,
            total_seconds_watched=0
        )

        # /api/v1/user/videos

        data = """
[
   {
        "completed": false, 
        "duration": 172, 
        "kind": "UserVideo", 
        "last_second_watched": 20, 
        "last_watched": "2011-05-04T06:01:47Z", 
        "points": 44, 
        "seconds_watched": 10, 
        "user": "you@gmail.com",
        "video": {
            "date_added": "2011-03-04T06:01:47Z", 
            "description": "U03_L2_T2_we1 Multiplying Decimals", 
            "duration": 172, 
            "ka_url": "http://www.khanacademy.org/video/multiplying-decimals", 
            "keywords": "U03_L2_T2_we1, Multiplying, Decimals", 
            "kind": "Video", 
            "playlists": [
                "Developmental Math"
            ], 
            "readable_id": "multiplying-decimals", 
            "title": "Multiplying Decimals", 
            "url": "http://www.youtube.com/watch?v=JEHejQphIYc&feature=youtube_gdata_player", 
            "views": 9837, 
            "youtube_id": "JEHejQphIYc"
        }
    }
]
        """

        video_watch = Video.objects.load(json.loads(data), user)[0]
        self.assertEqual(
            Watch.objects.get(user=user, video=video_watch.video),
            video_watch
        )
        self.assertEqual(video_watch.seconds_watched, 10)

    def test_load_exercise_performance(self):
        from khan.models import Exercise, UserData, Performance

        user = UserData.objects.create(
            nickname='test',
            user_id='you@gmail.com',
            prettified_user_email='',
            joined=timezone.now(),
            last_activity=timezone.now(),
            points=0,
            total_seconds_watched=0
        )

        exercise = Exercise.objects.create(
            name='',
            short_name='',
            description='',
            live=False,
            summative=False,
            khan_id='subtraction_1',
            url='',
            h_position=0,
            v_position=0,
            seconds_per_fast_problem=0
        )

        # /api/v1/user/exercises
        
        data = """
[
    {
        "exercise": "subtraction_1", 
        "first_done": "2011-05-01T06:01:47Z", 
        "kind": "UserExercise", 
        "last_done": "2011-05-04T06:01:47Z", 
        "last_review": "2011-05-02T06:01:47Z", 
        "longest_streak": 26, 
        "proficient_date": "2011-05-03T06:01:47Z", 
        "seconds_per_fast_problem": 4.0, 
        "streak": 26, 
        "summative": false, 
        "total_done": 26, 
        "user": "you@gmail.com"
    }
]
        """

        performance = Exercise.objects.load(json.loads(data), user)[0]
        self.assertEqual(
            Performance.objects.get(user=user, exercise=exercise),
            performance
        )
        self.assertEqual(performance.exercise, exercise)
        self.assertEqual(performance.streak, 26)

    def test_load_userdata(self):
        from khan.models import UserData, Exercise

        Exercise.objects.create(
            name='',
            short_name='',
            description='',
            live=False,
            summative=False,
            khan_id='addition_1',
            url='',
            h_position=0,
            v_position=0,
            seconds_per_fast_problem=0
        )

        data = """
{
    "all_proficient_exercises": [
        "addition_1", 
        "subtraction_1", 
        "multiplication_0.5"
    ], 
    "badge_counts": {
        "0": 1, 
        "1": 1, 
        "2": 0, 
        "3": 0, 
        "4": 0, 
        "5": 1
    }, 
    "coaches": [
        "yourcoach@gmail.com"
    ], 
    "joined": "2011-02-04T06:01:47Z", 
    "kind": "UserData", 
    "last_activity": "2011-05-04T06:01:47Z", 
    "nickname": "Gob Bluth",
    "points": 9188, 
    "proficient_exercises": [
        "addition_1", 
        "subtraction_1", 
        "multiplication_0.5"
    ], 
    "suggested_exercises": [
        "addition_2", 
        "subtraction_2"
    ], 
    "total_seconds_watched": 105, 
    "user_id": "you@gmail.com", 
    "prettified_user_email": "you@gmail.com"    
}
"""
        user = UserData.objects.load(json.loads(data))
        self.assertEqual(1, len(user.proficient_exercises.all()))
        self.assertEqual('Gob Bluth', user.nickname)

    def test_root_topic_loading(self):
        from khan.models import Topic
        data = """
{
  "children": [],
  "description": "All concepts fit into the root of all knowledge",
  "extended_slug": "root",
  "hide": true,
  "id": "root",
  "ka_url": "http://www.khanacademy.org/#root",
  "kind": "Topic",
  "relative_url": "/#root",
  "standalone_title": "The Root of All Knowledge",
  "tags": [],
  "title": "The Root of All Knowledge",
  "topic_page_url": "/root"
}
        """

        topic = Topic.objects.load(json.loads(data))
        self.assertEqual(0, len(topic.subtopics.all()))
        self.assertEqual('root', topic.khan_id)
        self.assertEqual('http://www.khanacademy.org/#root', topic.url)
        self.assertEqual('The Root of All Knowledge', topic.title)
        self.assertEqual('All concepts fit into the root of all knowledge', topic.description)
