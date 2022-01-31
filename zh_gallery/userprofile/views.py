from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_account(request):
    return render(request, 'userprofile/my_account.html')
