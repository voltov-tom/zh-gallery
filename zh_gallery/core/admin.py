from django.contrib import admin
from .models import MainCategory, MediaItem, SubCategory, MediaItemReview, About


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    exclude = ('slug',)


admin.site.register(MediaItemReview)
admin.site.register(About)
