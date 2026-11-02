"""Админка: списки с annotate-счётчиками, поиск и автодополнение."""

from __future__ import annotations

from django.contrib import admin
from django.db.models import Count
from modeltranslation.admin import TranslationAdmin

from .models import About, MainCategory, MediaItem, MediaItemReview, SubCategory


@admin.register(MainCategory)
class MainCategoryAdmin(TranslationAdmin):
    list_display = ("title", "slug", "subcategories_count")
    list_display_links = ("title",)
    search_fields = ("title", "slug")
    readonly_fields = ("slug",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(_subcategories_count=Count("subcategories", distinct=True))
        )

    @admin.display(description="Подкатегорий", ordering="_subcategories_count")
    def subcategories_count(self, obj: MainCategory) -> int:
        return obj._subcategories_count


@admin.register(SubCategory)
class SubCategoryAdmin(TranslationAdmin):
    list_display = ("title", "category", "slug", "media_items_count")
    list_display_links = ("title",)
    list_filter = ("category",)
    search_fields = ("title", "slug", "description")
    autocomplete_fields = ("category",)
    readonly_fields = ("slug",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("category")
            .annotate(_media_items_count=Count("media_items", distinct=True))
        )

    @admin.display(description="Элементов", ordering="_media_items_count")
    def media_items_count(self, obj: SubCategory) -> int:
        return obj._media_items_count


@admin.register(MediaItem)
class MediaItemAdmin(TranslationAdmin):
    list_display = (
        "title",
        "subcategory",
        "slug",
        "views",
        "likes_count",
        "reviews_count",
        "like_time",
    )
    list_display_links = ("title",)
    list_filter = ("subcategory__category", "subcategory")
    search_fields = ("title", "slug", "description")
    autocomplete_fields = ("subcategory",)
    readonly_fields = ("slug", "views", "like_time")
    date_hierarchy = None

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("subcategory", "subcategory__category")
            .annotate(
                _likes_count=Count("likes", distinct=True),
                _reviews_count=Count("reviews", distinct=True),
            )
        )

    @admin.display(description="Лайков", ordering="_likes_count")
    def likes_count(self, obj: MediaItem) -> int:
        return obj._likes_count

    @admin.display(description="Комментариев", ordering="_reviews_count")
    def reviews_count(self, obj: MediaItem) -> int:
        return obj._reviews_count


@admin.register(MediaItemReview)
class MediaItemReviewAdmin(admin.ModelAdmin):
    list_display = ("media_item", "user", "date_added", "edited", "short_content")
    list_filter = ("edited", "date_added")
    search_fields = ("content", "media_item__title", "user__username")
    autocomplete_fields = ("media_item", "user")
    readonly_fields = ("date_added",)

    @admin.display(description="Текст")
    def short_content(self, obj: MediaItemReview) -> str:
        return obj.content[:80]


@admin.register(About)
class AboutAdmin(TranslationAdmin):
    """Страница «О проекте» — единственная запись, поэтому лишние кнопки скрыты."""

    def has_add_permission(self, request) -> bool:
        return not About.objects.exists()
