"""HTML-страницы галереи.

Чтение отдаём CBV, а всю работу с ORM — селекторам (core/selectors.py) и
сервисам (core/services.py). Никакой логики в шаблонах и вьюхах не остаётся.
"""

from __future__ import annotations

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import DetailView

from core import selectors, services
from core.forms import ReviewForm
from core.models import MainCategory, MediaItem, SubCategory


class WithBackUrlMixin:
    """Добавляет в контекст ссылку «назад» для parts/back_button_title.html."""

    back_url_name: str = "frontpage_view"

    def get_back_url(self) -> str:
        return reverse(self.back_url_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("back_url", self.get_back_url())
        return context


class MainCategoryDetailView(WithBackUrlMixin, DetailView):
    """Страница категории: список подкатегорий с суммарной статистикой."""

    model = MainCategory
    template_name = "core/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subcategories"] = selectors.subcategories_with_stats(self.object)
        return context


class SubCategoryDetailView(WithBackUrlMixin, DetailView):
    """Страница подкатегории: сетка медиа-элементов.

    Ищем по паре (категория, slug): раньше достаточно было одного slug, и
    подкатегория открывалась по чужому адресу, если слаги пересекались.
    """

    model = SubCategory
    template_name = "core/subcategory_detail.html"
    context_object_name = "subcategory"

    def get_queryset(self):
        return SubCategory.objects.select_related("category").filter(
            category__slug=self.kwargs["category_slug"]
        )

    def get_back_url(self) -> str:
        return self.object.category.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_items"] = selectors.media_items_with_stats(self.object)
        return context


class MediaItemDetailView(WithBackUrlMixin, DetailView):
    """Страница элемента: счётчик просмотров, лайки и комментарии."""

    model = MediaItem
    template_name = "core/media_item_detail.html"
    context_object_name = "media_item"
    form_class = ReviewForm

    def get_queryset(self):
        return MediaItem.objects.with_stats().filter(
            subcategory__category__slug=self.kwargs["category_slug"],
            subcategory__slug=self.kwargs["subcategory_slug"],
        )

    def get_back_url(self) -> str:
        return self.object.subcategory.get_absolute_url()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        services.register_view(self.object)
        return self.render_to_response(self.get_context_data(object=self.object))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            # Форма комментария видна только авторизованным
            query = urlencode({"next": request.path})
            return redirect(f"{reverse('account_login')}?{query}")

        form = self.form_class(request.POST)
        if form.is_valid():
            services.create_review(
                media_item=self.object,
                user=request.user,
                content=form.cleaned_data["content"],
            )
            return redirect(self.object.get_absolute_url())

        return self.render_to_response(self.get_context_data(object=self.object, form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", self.form_class())
        context["likes_count"] = getattr(self.object, "likes_count", self.object.likes.count())
        context["already_liked"] = (
            self.request.user.is_authenticated
            and self.object.likes.filter(pk=self.request.user.pk).exists()
        )
        context.update(selectors.media_item_neighbours(self.object))
        return context
