from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import MainCategory, MediaItem, SubCategory, MediaItemReview, About


class MainCategoryAdmin(TranslationAdmin):
    pass


class SubCategoryAdmin(TranslationAdmin):
    pass


class MediaItemAdmin(TranslationAdmin):
    pass


class AboutAdmin(TranslationAdmin):
    pass


admin.site.register(MediaItemReview)
admin.site.register(About, AboutAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(MediaItem, MediaItemAdmin)
