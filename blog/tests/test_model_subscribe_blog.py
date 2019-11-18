from django.test import TestCase
from django.utils import timezone
from blog.models import SubscribeBlog

class SubscribeBlogTest(TestCase):
    def setUp(self):
        self.subscribe = SubscribeBlog.objects.create(email='a@a.com')

    def test_create(self):
        self.assertTrue(SubscribeBlog.objects.exists())

    def test_created_at(self):
        """SubscribeBlog must have an auto created_at attr"""
        self.assertIsInstance(self.subscribe.created_at, timezone.datetime)