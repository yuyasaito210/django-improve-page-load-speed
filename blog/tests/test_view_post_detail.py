from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from model_mommy import mommy
from blog.models import Post


class PostDetail(TestCase):
    def setUp(self):
        author = mommy.make(get_user_model())
        self.post = Post.objects.create(
            author = author,
            title = 'title',
            text = 'text',
        )
        self.response = self.client.get(r('blog:post-detail', self.post.slug))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'post/detail.html')

    def test_context(self):
        variables = ['post', 'popular_posts']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)
