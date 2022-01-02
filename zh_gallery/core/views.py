from django.shortcuts import render, get_object_or_404
from .models import MainCategory, MediaItem, SubCategory


def frontpage_view(request):
    return render(request, 'frontpage.html')


def about_view(request):
    return render(request, 'about.html')


def category_view(request, slug):
    category = get_object_or_404(MainCategory, slug=slug)
    content = {
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
