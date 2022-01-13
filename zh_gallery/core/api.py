import json

from django.http import JsonResponse

from .models import MediaItem


def like(request):
    data = json.loads(request.body)
    print(data['slug'])
    media_item = MediaItem.objects.filter(slug=data['slug'])
    media_item.likes.add(request.user)
    print('request.user:', request.user, 'media_item:', media_item)

    return JsonResponse({'success': True})
