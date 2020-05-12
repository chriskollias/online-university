from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from online_university.permissions import group_required
from .forms import *

@group_required('Admin')
def admin_portal_home_view(request, *args, **kwargs):
    return render(request, 'admin_portal/admin_portal_home.html', {})

@group_required('Admin')
def create_user_view(request, *args, **kwargs):
    if request.method == 'POST':
        base_form = UserCreationForm(request.POST)
        extended_form = AdminCreateUserForm(request.POST)
        if base_form.is_valid() and extended_form.is_valid():
            user_type = extended_form.cleaned_data['user_type']
            first_name = extended_form.cleaned_data['first_name']
            last_name = extended_form.cleaned_data['last_name']
            email = extended_form.cleaned_data['email']
            print('User type is ', user_type)
            new_user = base_form.save()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.save()
            #new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            if user_type == 'Admin':
                admin_group, created = Group.objects.get_or_create(name='Admin')
                new_user.groups.add(admin_group)
            elif user_type == 'Instructor':
                instructor_group, created = Group.objects.get_or_create(name='Instructor')
                new_user.groups.add(instructor_group)
            elif user_type == 'Student':
                student_group, created = Group.objects.get_or_create(name='Student')
                new_user.groups.add(student_group)
            else:
                print('Error - invalid user_type, could not add user to user group.')
            # TODO: insert success message here
            return redirect('admin-home') # will want to redirect elsewhere most likely, e.g. list of users
        else:
            print(base_form.errors)
            print(extended_form.errors)
            return render(request, 'admin_portal/create_user.html', {'base_form': base_form, 'extended_form': extended_form})

    base_form = UserCreationForm()
    extended_form = AdminCreateUserForm()
    return render(request, 'admin_portal/create_user.html', {'base_form': base_form, 'extended_form': extended_form})

