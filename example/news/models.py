import datetime

from django.db import models
from django.core.urlresolvers import reverse

from featured_item.fields import FeaturedField

class Story(models.Model):

    title = models.CharField(max_length=255)
    body = models.TextField()

    created = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(default=datetime.datetime.now)

    story_of_the_day = FeaturedField()
    story_of_the_week = FeaturedField()

    class Meta:
        ordering = ['-published']
        verbose_name_plural = 'stories'

    def get_absolute_url(self):
        return reverse('news.story_detail', kwargs={
            'story_pk': self.pk,
        })

    def __unicode__(self):
        return self.title
