from .models import MainCategory


def categories(request):
    categories = MainCategory.objects.all()
    context = {
        'categories': categories
    }
    return context
