from django.contrib import admin

from news.models import Story

class StoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'story_of_the_day',
        'story_of_the_week',
    )

admin.site.register(Story, StoryAdmin)
