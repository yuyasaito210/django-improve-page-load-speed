from django.db import models


class PostManager(models.Manager):
    def published(self):
        return self.filter(published_date__isnull=False)