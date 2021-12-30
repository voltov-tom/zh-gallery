from .models import MainCategory


def categories(request):
    categories = MainCategory.objects.all()
    return {'categories': categories}
