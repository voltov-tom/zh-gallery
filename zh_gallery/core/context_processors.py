from .models import MainCategory, SubCategory
from zh_gallery import settings


def categories(request):
    categories = MainCategory.objects.all()
    client_id = settings.OAuth_google
    context = {
        'client_id': client_id,
        'categories': categories
    }
    return context
