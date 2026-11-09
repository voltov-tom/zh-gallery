"""Тесты HTML-страниц."""

from __future__ import annotations

import pathlib

import pytest
from django.conf import settings
from django.urls import reverse

from core.models import MediaItem, MediaItemReview, SubCategory
from core.tests.conftest_helpers import make_image_file


@pytest.mark.django_db
def test_frontpage_renders_without_data(client):
    response = client.get(reverse("frontpage_view"))
    assert response.status_code == 200
    assert b"vue" not in response.content.lower()


@pytest.mark.django_db
def test_frontpage_shows_reviews_and_liked_items(client, media_item, review, user):
    media_item.likes.add(user)

    response = client.get(reverse("frontpage_view"))

    assert response.status_code == 200
    assert review.content.encode() in response.content
    assert media_item.title.encode() in response.content


@pytest.mark.django_db
def test_category_page_shows_stats(client, category, subcategory, media_item, user):
    media_item.likes.add(user)

    response = client.get(category.get_absolute_url())

    assert response.status_code == 200
    assert subcategory.title.encode() in response.content
    assert b"views_likes" in response.content


@pytest.mark.django_db
def test_subcategory_page_renders_grid(client, subcategory, media_item):
    response = client.get(subcategory.get_absolute_url())

    assert response.status_code == 200
    assert media_item.title.encode() in response.content


@pytest.mark.django_db
def test_subcategory_from_other_category_is_404(client, category, subcategory, media_item):
    other = SubCategory.objects.create(category=category, title="Пейзажи")
    url = f"/{other.slug}/{subcategory.slug}/"

    assert client.get(url).status_code == 404


@pytest.mark.django_db
def test_media_item_page_increments_views(client, media_item):
    response = client.get(media_item.get_absolute_url())

    media_item.refresh_from_db()
    assert response.status_code == 200
    assert media_item.views == 1


@pytest.mark.django_db
def test_media_item_page_404_for_wrong_category(client, media_item):
    url = f"/wrong/{media_item.subcategory.slug}/{media_item.slug}/"
    assert client.get(url).status_code == 404


@pytest.mark.django_db
def test_authenticated_user_can_leave_review(client, media_item, user):
    client.force_login(user)

    response = client.post(media_item.get_absolute_url(), {"content": "Отличная работа"})

    assert response.status_code == 302
    assert MediaItemReview.objects.filter(content="Отличная работа").exists()


@pytest.mark.django_db
def test_empty_review_is_rejected(client, media_item, user):
    client.force_login(user)

    response = client.post(media_item.get_absolute_url(), {"content": "   "})

    assert response.status_code == 200
    assert MediaItemReview.objects.count() == 0
    assert b"help is-danger" in response.content


@pytest.mark.django_db
def test_anonymous_post_is_redirected_to_login(client, media_item):
    response = client.post(media_item.get_absolute_url(), {"content": "аноним"})

    assert response.status_code == 302
    assert reverse("account_login") in response["Location"]
    assert MediaItemReview.objects.count() == 0


@pytest.mark.django_db
def test_about_page_shows_body(client, about):
    response = client.get(reverse("about_view"))

    assert response.status_code == 200
    assert "О проекте".encode() in response.content


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name", ["terms_and_conditions_view", "privacy_policy_view", "robots_txt", "healthcheck"]
)
def test_simple_pages_respond(client, name):
    assert client.get(reverse(name)).status_code == 200


@pytest.mark.django_db
def test_sitemap_contains_media_item(client, media_item):
    response = client.get(reverse("django.contrib.sitemaps.views.sitemap"))

    assert response.status_code == 200
    assert media_item.get_absolute_url().encode() in response.content


@pytest.mark.django_db
def test_media_item_detail_uses_annotated_counters(client, media_item, user):
    media_item.likes.add(user)

    response = client.get(media_item.get_absolute_url())

    assert response.context["likes_count"] == 1
    assert response.context["already_liked"] is False


@pytest.mark.django_db
def test_detail_page_has_no_vue_markup(client, media_item):
    response = client.get(media_item.get_absolute_url())
    assert b"new Vue" not in response.content
    assert b"[[" not in response.content


@pytest.mark.django_db
def test_reviews_are_escaped(client, media_item, user):
    MediaItemReview.objects.create(
        media_item=media_item, user=user, content="<script>alert(1)</script>"
    )

    response = client.get(media_item.get_absolute_url())

    assert b"<script>alert(1)</script>" not in response.content
    assert b"&lt;script&gt;" in response.content


@pytest.mark.django_db
def test_missing_media_item_is_404(client, subcategory):
    assert client.get(f"/{subcategory.category.slug}/{subcategory.slug}/nope/").status_code == 404


@pytest.mark.django_db
def test_subcategory_page_does_not_duplicate_media_items(client, subcategory, user):
    item = MediaItem(subcategory=subcategory, title="Раз")
    item.image.save("one.jpg", make_image_file("one.jpg"), save=True)
    item.likes.add(user)
    MediaItemReview.objects.create(media_item=item, user=user, content="ок")

    response = client.get(subcategory.get_absolute_url())

    # название встречается и в alt картинки, поэтому считаем именно заголовок карточки
    assert response.content.count(f">{item.title}<".encode()) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name",
    [
        "frontpage_view",
        "about_view",
        "terms_and_conditions_view",
        "privacy_policy_view",
        "account_login",
        "account_signup",
        "account_reset_password",
    ],
)
def test_no_raw_template_comments(client, name):
    """`{# … #}` в Django однострочный: многострочный комментарий утекает в текст."""
    response = client.get(reverse(name))

    assert b"{#" not in response.content
    assert b"#}" not in response.content


@pytest.mark.django_db
def test_footer_uses_local_social_icons(client):
    response = client.get(reverse("about_view"))

    # Instagram убран из футера — остались VK и X; внешних хотлинков нет
    assert response.content.count(b'class="footer-social__link"') == 2
    assert b"instagram" not in response.content.lower()
    assert b"upload.wikimedia.org" not in response.content


@pytest.mark.django_db
def test_catalog_pages_have_no_leaked_template_comments(client, category, subcategory, media_item):
    """Комментарии {# … #} в партиалах карточек не должны попадать в сетку."""
    for url in (category.get_absolute_url(), subcategory.get_absolute_url()):
        content = client.get(url).content
        assert b"{#" not in content, url
        assert b"#}" not in content, url


@pytest.mark.django_db
def test_like_icons_are_vector_and_match_style(client, media_item, user):
    """Сердце и глаз — одно семейство SVG-иконок; растровые PNG/GIF не используются."""
    media_item.likes.add(user)
    client.force_login(user)

    content = client.get(media_item.get_absolute_url()).content

    assert b"heart-fill.svg" in content  # состояние «лайк поставлен»
    assert b"heart-outline.svg" in content  # состояние «не лайкнуто»
    assert b"eye-outline.svg" in content
    assert b"like-pink" not in content
    assert b"dislike-pink" not in content
    assert b"like.GIF" not in content


@pytest.mark.django_db
def test_terms_page_is_localised(client):
    ru = client.get(reverse("terms_and_conditions_view"), headers={"accept-language": "ru"})
    en = client.get(reverse("terms_and_conditions_view"), headers={"accept-language": "en"})

    assert ru.status_code == en.status_code == 200
    assert "Гражданского кодекса".encode() in ru.content
    assert "Редакция от".encode() in ru.content
    assert b"Civil Code" in en.content
    assert b"Last updated" in en.content
    assert "Гражданского кодекса".encode() not in en.content


@pytest.mark.django_db
def test_privacy_page_is_localised(client):
    ru = client.get(reverse("privacy_policy_view"), headers={"accept-language": "ru"})
    en = client.get(reverse("privacy_policy_view"), headers={"accept-language": "en"})

    assert ru.status_code == en.status_code == 200
    assert "152-ФЗ".encode() in ru.content
    assert b"152-FZ" in en.content
    assert "Персональных данных".encode() not in en.content


@pytest.mark.django_db
def test_media_item_page_has_hover_zoom(client, media_item):
    """Наведение мыши увеличивает картинку — без клика по элементам."""
    content = client.get(media_item.get_absolute_url()).content

    assert b"data-media-zoom" in content
    assert b"media-zoom__image" in content
    assert b"core/js/zoom.js" in content


@pytest.mark.django_db
def test_grid_cards_do_not_zoom(client, subcategory, media_item):
    """Зум только на странице работы, чтобы сетка не дёргалась."""
    assert b"data-media-zoom" not in client.get(subcategory.get_absolute_url()).content


@pytest.mark.django_db
def test_css_is_served_locally(client):
    """Стили не тянутся с внешних CDN: Bulma лежит в статике, шрифты Google убраны."""
    content = client.get(reverse("frontpage_view")).content

    assert b"core/vendor/bulma.min.css" in content
    assert b"cdn.jsdelivr.net" not in content
    assert b"fonts.googleapis.com" not in content
    assert b"fonts.gstatic.com" not in content


@pytest.mark.django_db
def test_footer_email_is_mailto_link(client):
    """Клик по адресу должен открывать почтовую программу (mailto:)."""
    content = client.get(reverse("frontpage_view")).content

    assert b'href="mailto:zhenya@zh-gallery.ru"' in content


@pytest.mark.django_db
def test_footer_has_no_appgallery_link(client):
    """Бейдж AppGallery убран из футера."""
    content = client.get(reverse("frontpage_view")).content

    assert b"appgallery" not in content.lower()
    assert b"consumer-tkbdownload.huawei.com" not in content


def test_zoom_hint_is_hidden_on_touch():
    """На телефоне наведения нет — подсказка «наведите курсор» не показывается."""
    css = (pathlib.Path(settings.BASE_DIR) / "core/static/core/css/components.css").read_text()

    assert "(hover: none)" in css
    assert "(pointer: coarse)" in css
    assert ".media-zoom__hint {" in css


def test_zoom_js_is_disabled_without_hover():
    """На тач-устройствах зум не подключается: тап не должен увеличивать картинку."""
    js = (pathlib.Path(settings.BASE_DIR) / "core/static/core/js/zoom.js").read_text()

    assert "supportsHover" in js
    assert "(hover: hover) and (pointer: fine)" in js


@pytest.mark.django_db
def test_ai_badge_is_shown_for_generated_description(client, media_item):
    media_item.description_generated_by_ai = True
    media_item.save(update_fields=["description_generated_by_ai"])

    content = client.get(media_item.get_absolute_url()).content

    # .mo в тестах не собирается, поэтому проверяем разметку плашки
    assert b"ai-badge" in content
    assert b"sparkles-outline" in content


@pytest.mark.django_db
def test_ai_badge_is_hidden_for_manual_description(client, media_item):
    content = client.get(media_item.get_absolute_url()).content

    assert b"ai-badge" not in content
