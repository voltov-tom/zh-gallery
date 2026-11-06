"""Админка: списки с annotate-счётчиками, поиск и автодополнение."""

from __future__ import annotations

from django.conf import settings
from django.contrib import admin, messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path
from modeltranslation.admin import TranslationAdmin

from .integrations.ai import AIDescriptionError
from .models import About, MainCategory, MediaItem, MediaItemReview, SubCategory
from .services import generate_media_description


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
    change_form_template = "admin/core/mediaitem/change_form.html"
    actions = ("generate_description_action",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = {**(extra_context or {}), "ai_enabled": bool(settings.AI_API_KEY)}
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        return [
            path(
                "<int:pk>/generate-description/",
                self.admin_site.admin_view(self.generate_description_view),
                name="core_mediaitem_generate_description",
            ),
            *super().get_urls(),
        ]

    def generate_description_view(self, request, pk):
        """Кнопка «Сгенерировать описание» на странице работы."""
        media_item = get_object_or_404(MediaItem, pk=pk)
        try:
            generate_media_description(media_item)
        except AIDescriptionError as error:
            self.message_user(request, f"Описание не создано: {error}", level=messages.ERROR)
        else:
            self.message_user(request, "Описание сгенерировано", level=messages.SUCCESS)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") or request.path)

    @admin.action(description="Сгенерировать описание через ИИ")
    def generate_description_action(self, request, queryset):
        """Пакетная генерация для выбранных работ в списке."""
        if not settings.AI_API_KEY:
            self.message_user(request, "AI_API_KEY не задан — генерация отключена", level=messages.ERROR)
            return

        done = failed = 0
        for media_item in queryset:
            try:
                generate_media_description(media_item)
            except AIDescriptionError as error:
                failed += 1
                self.message_user(
                    request, f"«{media_item.title}»: {error}", level=messages.WARNING
                )
            else:
                done += 1
        if done:
            self.message_user(request, f"Описаний создано: {done}", level=messages.SUCCESS)
        if failed:
            self.message_user(request, f"Не удалось: {failed}", level=messages.WARNING)

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
