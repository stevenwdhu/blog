from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

from taggit.managers import TaggableManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from ckeditor.fields import RichTextField
from mdeditor.fields import MDTextField


def set_default_column():
    return ArticleColumn.objects.get_or_create(title='Misc')[0].id


class ArticleColumn(models.Model):
    title = models.CharField(max_length=100)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='anonymous')
    column = models.ForeignKey(ArticleColumn, on_delete=models.SET_DEFAULT, default=set_default_column)
    title = models.CharField(max_length=100)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    # body = models.TextField()
    body = MDTextField()
    views = models.PositiveIntegerField(default=0)
    tag = TaggableManager(blank=True)
    likes = models.PositiveIntegerField(default=0)
    image = ProcessedImageField(upload_to='article/',
                                processors=[ResizeToFit(width=400)],
                                # format='JPEG',
                                options={'quality': 100},
                                blank=True
                                )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article-detail', kwargs={'pk': self.pk})
