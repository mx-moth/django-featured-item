from django.shortcuts import get_object_or_404, render

from news.models import Story

def news_story_list(request):
    story_list = Story.objects.all()[:10]

    try:
        story_of_the_day = Story.objects.get(story_of_the_day=True)
    except Story.DoesNotExist:
        story_of_the_day = None

    try:
        story_of_the_week = Story.objects.get(story_of_the_week=True)
    except Story.DoesNotExist:
        story_of_the_week = None

    return render(request, 'news/story_list.html', {
        'story_list': story_list,
        'story_of_the_day': story_of_the_day,
        'story_of_the_week': story_of_the_week,
    })

def news_story_detail(request, story_pk):
    story_item = get_object_or_404(Story, pk=story_pk)

    return render(request, 'news/story_detail.html', {
        'story_item': story_item,
    })
