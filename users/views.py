from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
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
        base_form = UserCreationForm(request.POST)
        extended_form = ExtendedUserCreationForm(request.POST)
        if base_form.is_valid() and extended_form.is_valid():
            new_user = base_form.save()
            first_name = extended_form.cleaned_data['first_name']
            last_name = extended_form.cleaned_data['last_name']
            email = extended_form.cleaned_data['email']
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.save()
            student_group, created = Group.objects.get_or_create(name='Student')
            new_user.groups.add(student_group)
            messages.success(request, 'You have successfully created your account! You may now sign in.')
            return redirect('user-login')
        else:
            # TODO: properly handle user registration errors
            print(base_form.errors)
            form_errors = base_form.errors + extended_form.errors
            messages.warning(request, form_errors)
            return redirect('user-register')
    base_form = UserCreationForm()
    extended_form = ExtendedUserCreationForm()

    return render(request, 'users/register.html', {'base_form': base_form, 'extended_form': extended_form})


def user_edit_view(request, user_id, *args, **kwargs):
    user = get_object_or_404(User, pk=user_id)

    # check if logged in user has permission to edit this user's profile
    if not (request.user.groups.filter(name='Admin').exists() or request.user.pk == user_id):
        messages.warning(request, 'You do not have permission to view that page.')
        return redirect('landing-page')

    if request.method == 'POST':
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
