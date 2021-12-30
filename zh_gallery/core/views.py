from django.shortcuts import render, get_object_or_404
from .models import MainCategory, MediaItem


def frontpage_view(request):
    return render(request, 'frontpage.html')


def about_view(request):
    return render(request, 'about.html')


def category_view(request, slug):
    category = get_object_or_404(MainCategory, slug=slug)
    media_items = MediaItem.objects.all()
    content = {
        'media_items': media_items,
        'category': category
    }
    return render(request, 'category_detail.html', content)
