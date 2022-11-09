import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def my_account(request):
    user = request.user
    reviews_data = []

    for review in user.reviews.all():
        review_id = review.id
        media_item = review.media_item
        content = review.content
        date_added = review.date_added.strftime("%d.%m.%Y %H:%M")  # best to convert on the frontend
        edited = review.edited

        data = dict(
            id=review_id,
            user_id=user.id,
            media_item_title=media_item.title,
            media_item_url=str(media_item.get_absolute_url()),
            media_item_img=media_item.image.url,
            content=content,
            date_added=date_added,
            edited=edited
        )
        reviews_data.append(data)

    context = {
        'reviews_count': len(user.reviews.all()),
        'likes_count': len(user.likes.all()),
    }

    return render(request, 'userprofile/my_account.html', {'reviews_data': json.dumps(reviews_data), 'context': context})


def account(request, user_name):
    if str(request.user) == user_name:
        return redirect(my_account)

    user = get_object_or_404(User, username=user_name)
    reviews_data = []

    for review in user.reviews.all():
        review_id = review.id
        media_item = review.media_item
        content = review.content
        date_added = review.date_added.strftime("%d.%m.%Y %H:%M")  # best to convert on the frontend
        edited = review.edited

        data = dict(
            id=review_id,
            user_id=user.id,
            media_item_title=media_item.title,
            media_item_url=str(media_item.get_absolute_url()),
            media_item_img=media_item.image.url,
            content=content,
            date_added=date_added,
            edited=edited
        )
        reviews_data.append(data)

    context = {
        'username': user_name,
        'reviews_count': len(user.reviews.all()),
        'likes_count': len(user.likes.all()),
        'user_likes': user.likes.all(),
    }

    return render(request, 'userprofile/account.html', {'reviews_data': json.dumps(reviews_data), 'context': context})
