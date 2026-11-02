"""Страницы личного кабинета.

Раньше ``my_account`` и ``account`` дублировали друг друга построчно, собирали
JSON руками (``json.dumps`` + ``|safe`` в шаблоне — реальная XSS-дыра, так как
текст комментария пишет пользователь) и делали ``len(user.reviews.all())``.
Теперь это два тонких CBV, а разметку рендерит шаблон — JavaScript только
переключает режим редактирования и отправляет запросы.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from core import selectors

User = get_user_model()


def _profile_context(user) -> dict:
    """Общий контекст для «своего» и «чужого» профиля."""
    return {
        "reviews": selectors.reviews_of(user),
        "liked_items": selectors.liked_items_of(user),
    }


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = "userprofile/my_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_profile_context(self.request.user))
        return context


class AccountView(DetailView):
    model = User
    template_name = "userprofile/account.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "user_name"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated and request.user.pk == self.object.pk:
            return redirect("my_account_view")
        return self.render_to_response(self.get_context_data(object=self.object))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_profile_context(self.object))
        return context
