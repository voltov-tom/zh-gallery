import json

import requests
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import register
from django.views.decorators.cache import cache_control

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


@cache_control(max_age=3600)
def nextcloud_proxy(request, path):
    """
    Проксирует запросы к файлам из Nextcloud
    """
    config = getattr(settings, 'NEXTCLOUD_CONFIG', {})

    if not config:
        raise Http404("Nextcloud не настроен")

    # Формируем URL к Nextcloud
    webdav_root = config.get('webdav_root', '').rstrip('/')
    if webdav_root and not path.startswith(webdav_root):
        full_path = f"{webdav_root}/{path}"
    else:
        full_path = path

    # Убираем начальный слэш если есть
    if full_path.startswith('/'):
        full_path = full_path[1:]

    nextcloud_url = f"{config.get('webdav_hostname', '').rstrip('/')}/{full_path}"

    # Аутентификация
    auth = (config.get('webdav_login', ''), config.get('webdav_password', ''))

    try:
        # Загружаем файл из Nextcloud
        response = requests.get(nextcloud_url, auth=auth, stream=True, timeout=30)

        if response.status_code != 200:
            raise Http404("Файл не найден")

        # Возвращаем ответ с правильными заголовками
        django_response = HttpResponse(
            response.iter_content(chunk_size=8192),
            content_type=response.headers.get('Content-Type', 'application/octet-stream')
        )

        # Копируем некоторые заголовки
        if 'Content-Length' in response.headers:
            django_response['Content-Length'] = response.headers['Content-Length']
        return django_response

    except requests.RequestException as e:
        raise Http404("Файл не найден")
