from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from blog.utils.slugify import generate_unique_slug
from blog.managers import PostManager


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name = 'author',
        on_delete = models.PROTECT
    )
    image = models.ImageField(upload_to='posts', blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField('slug', unique=True, editable=False, max_length=300)
    text = RichTextUploadingField()
    hit = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post-detail', args = [self.slug])

    def save(self, *args, **kwargs):
        # Edit
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        # Create
        else:
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save(*args, **kwargs)


class SubscribeBlog(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)