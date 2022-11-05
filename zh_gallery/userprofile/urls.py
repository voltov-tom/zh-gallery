from django.urls import path

from .views import my_account, account

urlpatterns = [
    path('accounts/my-account/', my_account, name='my_account_view'),
    path('accounts/<slug:user_name>/', account, name='account_view'),
]
