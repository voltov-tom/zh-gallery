import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.template.defaulttags import register
from django.utils import timezone

from .models import MainCategory, MediaItem, SubCategory, MediaItemReview


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


def frontpage_view(request):
    last_reviews = MediaItemReview.objects.all()[:10]
    last_liked_items = MediaItem.objects.all().order_by('-like_time')[:10]

    context = {
        'last_reviews': last_reviews,
        'last_liked_items': last_liked_items
    }
    return render(request, 'frontpage.html', context)


def terms_and_conditions_view(request):
    return render(request, 'terms_and_conditions.html')


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')


def about_view(request):
    return render(request, 'about.html')


def category_view(request, slug):
    category = get_object_or_404(MainCategory, slug=slug)
    subcategories = SubCategory.objects.filter(category=category)

    views = {}
    likes = {}

    for sub in subcategories:
        media_items = MediaItem.objects.filter(subcategory=sub)

        category_views = sum(media_items.values_list('views', flat=True))
        views[sub] = category_views

        category_query = media_items.values_list('likes', flat=True)
        category_likes = 0
        for i in category_query:
            if i is not None:
                category_likes += 1
        likes[sub] = category_likes

    content = {
        'category': category,
        'subcategories': subcategories,
        'views': views,
        'likes': likes
    }
    return render(request, 'category_detail.html', content)


def subcategory_view(request, category_slug, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    media_items = MediaItem.objects.filter(subcategory=subcategory)
    content = {
        'subcategory': subcategory,
        'media_items': media_items
    }
    return render(request, 'subcategory_detail.html', content)


def media_item_view(request, category_slug, subcategory_slug, slug):
    media_item = get_object_or_404(MediaItem, slug=slug)
    media_item.views += 1
    media_item.save()

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '')
        MediaItemReview.objects.create(
            user=request.user,
            media_item=media_item,
            content=content
        )

        return redirect(
            'media_item_view',
            category_slug=category_slug,
            subcategory_slug=subcategory_slug,
            slug=slug
        )

    already_liked = media_item.likes.filter(id=request.user.id).exists()

    content = {
        'media_item': media_item,
        'already_liked': json.dumps(already_liked),
        'likes_count': media_item.total_likes
    }
    return render(request, 'media_item_detail.html', content)


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
