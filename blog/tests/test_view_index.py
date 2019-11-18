from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.utils import timezone
from model_mommy import mommy
from blog.models import Post, SubscribeBlog


class IndexGet(TestCase):
    def setUp(self):
        self.published_post = mommy.make(Post, text='text', published_date=timezone.now())
        self.unpublished_post = mommy.make(Post, text='text')
        self.response = self.client.get(r('blog:posts'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'post/list.html')

    def test_context(self):
        variables = ['posts', 'popular_posts']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)

    def test_html(self):
        """Must show only published posts."""
        contents_that_should_be_shown = [
            self.published_post.title,
        ]

        for expected in contents_that_should_be_shown:
            with self.subTest():
                self.assertContains(self.response, expected)

        contents_that_should_not_be_shown = [
            self.unpublished_post.title,
        ]

        for expected in contents_that_should_not_be_shown:
            with self.subTest():
                self.assertNotContains(self.response, expected)


class IndexPost(TestCase):
    def setUp(self):
        data = dict(
            email = 'email@email.com',
        )
        self.response = self.client.post(r('blog:posts'), data)

    def test_post(self):
        self.assertTrue(SubscribeBlog.objects.exists())
