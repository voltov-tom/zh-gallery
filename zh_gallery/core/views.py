from django.shortcuts import render, get_object_or_404

from django.template.defaulttags import register

from .models import MainCategory, MediaItem, SubCategory


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
    subcategory = SubCategory.objects.filter(category=category)
    views = {}

    for sub in subcategory:
        media_items = MediaItem.objects.filter(subcategory=sub)
        category_views = sum(media_items.values_list('views', flat=True))
        views[sub] = category_views

    content = {
        'views': views,
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
    content = {
        'media_item': media_item
    }
    return render(request, 'media_item_detail.html', content)
