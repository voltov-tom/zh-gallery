"""Тесты HTML-страниц."""

from __future__ import annotations

import pytest
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
