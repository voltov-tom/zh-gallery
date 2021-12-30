from .models import MainCategory, SubCategory


def categories(request):
    categories = MainCategory.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        'categories': categories,
        'subcategories': subcategories
    }
    return context
