import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from slugify import slugify

from .models import MediaItem


def telegram_bot_get_media_item(request, media_item_name):
    slug = slugify(media_item_name)
    media_item = get_object_or_404(MediaItem, slug=slug)
    # media_item_url = request.get_host() + media_item.image.url
    media_item_url = 'https://zh-gallery.ru' + media_item.image.url
    return HttpResponse(json.dumps({'mediaItemUrl': media_item_url}), content_type='application/json')
