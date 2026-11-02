"""Простые информационные страницы."""

from __future__ import annotations

from django.views.generic import TemplateView

from core import selectors

from .gallery import WithBackUrlMixin


class FrontPageView(TemplateView):
    template_name = "core/frontpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_reviews"] = selectors.last_reviews()
        context["last_liked_items"] = selectors.recently_liked_items()
        return context


class AboutView(WithBackUrlMixin, TemplateView):
    """Страница «О проекте»; текст берётся из единственной записи About."""

    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # about уже приходит из контекст-процессора, но странице нужен именно он
        context["about"] = selectors.get_about()
        return context


class TermsAndConditionsView(WithBackUrlMixin, TemplateView):
    template_name = "core/terms_and_conditions.html"


class PrivacyPolicyView(WithBackUrlMixin, TemplateView):
    template_name = "core/privacy_policy.html"
