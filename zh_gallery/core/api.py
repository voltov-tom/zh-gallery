import json

from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import MediaItem, MediaItemReview


def like_button(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)

        if data['operation'] == 'like_submit':
            media_id = data['media_id']
            media_item = get_object_or_404(MediaItem, id=media_id)

            if media_item.likes.filter(id=request.user.id):
                media_item.likes.remove(request.user)
                liked = False
            else:
                if not media_item.likes:
                    media_item.likes.create()
                media_item.likes.add(request.user.id)
                media_item.like_time = timezone.now()
                media_item.save()
                liked = True

            context = {
                'likes_count': media_item.total_likes,
                'liked': liked,
                'media_id': media_id,
                'success': True
            }
            return HttpResponse(json.dumps(context), content_type='application/json')

    return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def edit_review(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)

        if data['operation'] == 'edit_review':
            review_id = data['review_id']
            user = request.user
            media_item_review = get_object_or_404(MediaItemReview, id=review_id, user=user)
            media_item_review.content = data['content']
            media_item_review.save()

            return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    return HttpResponse(json.dumps({'success': False}), content_type='application/json')


def delete_review(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)

        if data['operation'] == 'delete_review':
            review_id = data['review_id']
            user = request.user
            media_item_review = get_object_or_404(MediaItemReview, id=review_id, user=user)
            media_item_review.remove()

            return HttpResponse(json.dumps({'success': True}), content_type='application/json')

    return HttpResponse(json.dumps({'success': False}), content_type='application/json')
