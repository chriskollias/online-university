from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *

# needs logged in as admin required decorator
def admin_create_user_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print('User type is ', user_type)
            new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            new_user.save()

            if user_type == 'Admin':
                new_user_role = Admin(user=new_user)
            elif user_type == 'Instructor':
                new_user_role = Instructor(user=new_user)
            elif user_type == 'Student':
                new_user_role = Student(user=new_user)
            else:
                print('Error - invalid user_type')
            new_user_role.save()
            # insert success message here
            return redirect('landing-page') # will want to redirect elsewhere most likely, e.g. list of users
        else:
            print(form.errors)
            return render(request, 'users/admin_create_user.html', {'form': form})

    form = AdminCreateUserForm()
    return render(request, 'users/admin_create_user.html', {'form': form})


def user_register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('landing-page')

    form = UserCreationForm()
    return render(request, 'users/register.html', {})