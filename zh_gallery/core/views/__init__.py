"""Публичный интерфейс вьюх галереи (для core/urls.py)."""

from .gallery import MainCategoryDetailView, MediaItemDetailView, SubCategoryDetailView
from .health import healthcheck
from .media import media_file
from .pages import (
    AboutView,
    FrontPageView,
    PrivacyPolicyView,
    TermsAndConditionsView,
)

__all__ = [
    "AboutView",
    "FrontPageView",
    "MainCategoryDetailView",
    "MediaItemDetailView",
    "PrivacyPolicyView",
    "SubCategoryDetailView",
    "TermsAndConditionsView",
    "healthcheck",
    "media_file",
]
