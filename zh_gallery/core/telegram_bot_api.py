import json
from random import choice

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from slugify import slugify

from .models import MediaItem


def telegram_bot_get_media_item(request, media_item_name):
    slug = slugify(media_item_name)
    media_item = get_object_or_404(MediaItem, slug=slug)
    media_item_url = 'https://zh-gallery.ru' + media_item.image.url
    media_item.views += 1
    data = {
        'mediaItemUrl': media_item_url,
        'title': media_item.title,
        'likes': media_item.total_likes,
        'description': media_item.description,
        'views': media_item.views,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


def telegram_bot_get_random_item(request):
    media_items_keys = MediaItem.objects.values_list('pk', flat=True)
    random_media_item_pk = choice(media_items_keys)
    media_item = MediaItem.objects.get(pk=random_media_item_pk)
    media_item_url = 'https://zh-gallery.ru' + media_item.image.url
    media_item.views += 1
    data = {
        'mediaItemUrl': media_item_url,
        'title': media_item.title,
        'likes': media_item.total_likes,
        'description': media_item.description,
        'views': media_item.views
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
