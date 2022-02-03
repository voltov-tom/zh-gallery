import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_account(request):
    user = request.user
    reviews_data = []

    for review in user.reviews.all():
        review_id = review.id
        media_item = review.media_item
        content = review.content
        date_added = review.date_added

        data = dict(
            id=review_id,
            user_id=user.id,
            media_item=media_item,
            content=content,
            date_added=date_added
        )
        reviews_data.append(data)

    return render(request, 'userprofile/my_account.html', json.dumps(reviews_data))
