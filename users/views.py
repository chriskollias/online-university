from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *


def user_register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            # need to handle adding to user groups here

            return redirect('landing-page')

    form = UserCreationForm()
    return render(request, 'users/register.html', {})

# redirects the user to the proper portal after they login
def user_login_redirect(request, *args, **kwargs):
    # need to get which type of user it is
    # look into django groups
    pass