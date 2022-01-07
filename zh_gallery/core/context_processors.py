from .models import MainCategory, SubCategory


def categories(request):
    categories = MainCategory.objects.all()
    context = {
        'categories': categories
    }
    return context
