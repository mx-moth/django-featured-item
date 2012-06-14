from django.conf.urls import patterns, include, url

from news.views import news_story_list, news_story_detail

urlpatterns = patterns('',
    url(r'^$', news_story_list, name='news.story_list'),
    url(r'^story/(?P<story_pk>\d+)/$', news_story_detail, name='news.story_detail'),
)
