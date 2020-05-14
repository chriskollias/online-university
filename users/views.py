from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from online_university.permissions import group_required
from .forms import *
from .models import *


@group_required('Admin')
def all_users_view(request, *args, **kwargs):
    user_list = User.objects.all()
    return render(request, 'users/view_all_users.html', {'user_list': user_list})

def user_profile_view(request, user_id, *args, **kwargs):
    user = User.objects.get(pk=user_id)

    # check if the current user has permission to view this profile
    # admins can view all profiles, instructors and students can only view their own
    if request.user.groups.filter(name='Admin').exists() or request.user.pk == user_id:
        return render(request, 'users/user_profile.html', {'user': user})
    else:
        messages.warning(request, 'You do not have permission to view that page.')
        print('Warning sohuld be given')
        return redirect('landing-page')


def user_register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            # TODO: need to handle adding to user groups here

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
