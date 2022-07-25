import json

from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import register

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
    return render(request, 'core/frontpage.html', context)


def terms_and_conditions_view(request):
    return render(request, 'core/terms_and_conditions.html')


def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')


def about_view(request):
    return render(request, 'core/about.html')


def category_view(request, slug):
    category = get_object_or_404(MainCategory, slug=slug)
    subcategories = SubCategory.objects.filter(category=category)

    views = {}
    likes = {}
    reviews = {}

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

        category_query = media_items.values_list('reviews', flat=True)
        category_reviews = 0
        for i in category_query:
            if i is not None:
                category_reviews += 1
        reviews[sub] = category_reviews

    content = {
        'category': category,
        'subcategories': subcategories,
        'views': views,
        'likes': likes,
        'reviews': reviews
    }
    return render(request, 'core/category_detail.html', content)


def subcategory_view(request, category_slug, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    media_items = MediaItem.objects.filter(subcategory=subcategory)
    content = {
        'subcategory': subcategory,
        'media_items': media_items
    }
    return render(request, 'core/subcategory_detail.html', content)


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
    return render(request, 'core/media_item_detail.html', content)
