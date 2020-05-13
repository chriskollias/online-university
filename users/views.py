from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
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
    user = request.user
    messages.success(request, 'You have logged in.')
    if user.groups.filter(name='Admin').exists():
        return redirect('admin-home')
    elif user.groups.filter(name='Instructor').exists():
        return redirect('instructor-home')
    elif user.groups.filter(name='Student').exists():
        return redirect('student-home')
    else:
        return redirect('landing-page')


def user_logout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('landing-page')
