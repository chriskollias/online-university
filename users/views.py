from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from online_university.permissions import group_required
from .forms import ExtendedUserCreationForm


@group_required('Admin')
def all_users_view(request, *args, **kwargs):
    user_list = User.objects.all()
    return render(request, 'users/view_all_users.html', {'user_list': user_list})


def user_profile_view(request, user_id, *args, **kwargs):
    user = get_object_or_404(User, pk=user_id)

    # check if the current user has permission to view this profile
    # admins can view all profiles, instructors and students can only view their own
    if request.user.groups.filter(name='Admin').exists() or request.user.pk == user_id:
        return render(request, 'users/user_profile.html', {'user': user})
    else:
        messages.warning(request, 'You do not have permission to view that page.')
        return redirect('landing-page')


def user_register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            # TODO: need to handle adding to user groups here

            return redirect('landing-page')

    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_edit_view(request, user_id, *args, **kwargs):
    user = get_object_or_404(User, pk=user_id)

    print('Condition 1', request.user.groups.filter(name='Admin').exists())

    # check if logged in user has permission to edit this user's profile
    if not (request.user.groups.filter(name='Admin').exists() or request.user.pk == user_id):
        messages.warning(request, 'You do not have permission to view that page.')
        return redirect('landing-page')

    if request.method == 'POST':
        #base_form = UserCreationForm(request.POST, instance=user)
        extended_form = ExtendedUserCreationForm(request.POST)
        if extended_form.is_valid():
            user.first_name = extended_form.cleaned_data['first_name']
            user.last_name = extended_form.cleaned_data['last_name']
            user.email = extended_form.cleaned_data['email']
            user.save()
            messages.success(request, 'Profile has been successfully updated')
            return redirect(reverse('user-profile', kwargs={'user_id': user_id}))

    initial_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
    #base_form = UserCreationForm(instance=user)
    extended_form = ExtendedUserCreationForm(initial=initial_data)
    return render(request, 'users/edit_user.html', {'extended_form': extended_form, 'user': user})


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
