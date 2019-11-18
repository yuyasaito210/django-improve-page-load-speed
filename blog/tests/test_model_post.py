from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from model_mommy import mommy
from blog.models import Post
from blog.managers import PostManager


class PostModelTest(TestCase):
    def setUp(self):
        author = mommy.make(get_user_model())
        self.post = Post.objects.create(
            author = author,
            title = 'title',
            text = 'text',
        )

    def test_create(self):
        self.assertTrue(Post.objects.exists())

    def test_str(self):
        self.assertEqual('title', str(self.post))

    def test_image_can_be_blank(self):
        field = Post._meta.get_field('image')
        self.assertTrue(field.blank)
    
    def test_published_date_can_be_null(self):
        field = Post._meta.get_field('published_date')
        self.assertTrue(field.null)

    def test_created_at(self):
        """Post must have an auto created_at attr"""
        self.assertIsInstance(self.post.created_at, timezone.datetime)

    def test_slug_auto_generate(self):
        """Post must have an auto slugfield attr"""
        self.assertTrue(self.post.slug)

    def test_slug_unique(self):
        """Post must have a unique slugfield"""
        field = Post._meta.get_field('slug')
        self.assertTrue(field.unique)

    def test_post_cant_be_editable(self):
        """Post should not have an editable slug field."""
        field = Post._meta.get_field('slug')
        self.assertFalse(field.editable)


class PostManagerTest(TestCase):
    def setUp(self):
        mommy.make(Post, text='text', _quantity=5, published_date=timezone.now())
        mommy.make(Post, text='text', _quantity=5)

    def test_manager(self):
        self.assertIsInstance(Post.objects, PostManager)

    def test_all(self):
        qs = Post.objects.all()
        self.assertEqual(qs.count(), 10)

    def test_published(self):
        qs = Post.objects.published()
        self.assertEqual(qs.count(), 5)


class PostTestCase(TestCase):
    def setUp(self):
        self.post = mommy.make(Post, text='text')

    def test_publish(self):
        self.post.publish()
        self.assertIsNotNone(Post.objects.get(pk=self.post.pk).published_date)