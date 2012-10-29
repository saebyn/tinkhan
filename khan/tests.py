# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Unit tests for the `khan` Django app.
"""

import json

from django.test import TestCase


class DataLoadTest(TestCase):
    def test_load_userdata(self):
        from khan.models import UserData, Exercise

        Exercise.objects.create(name='', short_name='', description='', live=False, summative=False, khan_id='addition_1', url='', h_position=0, v_position=0, seconds_per_fast_problem=0)

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
