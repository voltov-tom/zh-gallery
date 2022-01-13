from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.template.defaulttags import register
from django.urls import reverse

from .models import MainCategory, MediaItem, SubCategory, MediaItemReview


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


def frontpage_view(request):
    return render(request, 'frontpage.html')


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
        # category_likes = sum(media_items.values_list('likes', flat=True))
        views[sub] = category_views
        # likes[sub] = category_likes

    content = {
        'subcategories': subcategories,
        'views': views,
        # 'likes': likes,
        'category': category
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
        print('post')
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

    content = {
        'media_item': media_item
    }
    return render(request, 'media_item_detail.html', content)
