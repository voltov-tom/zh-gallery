from .models import MainCategory, About


def context(request):
    categories = MainCategory.objects.all()
    description = About.objects.all()[0]
    ctx = {
        'categories': categories,
        'description': description
    }
    return ctx
