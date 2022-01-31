from django.urls import path

from .views import my_account

urlpatterns = [
    path('accounts/my-account/<str:username>', my_account, name='my_account_view'),
]
