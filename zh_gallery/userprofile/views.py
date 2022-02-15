import json

from django.shortcuts import render
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

    return render(request, 'userprofile/my_account.html', {'reviews_data': json.dumps(reviews_data)})
