from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import *

def admin_portal_home_view(request, *args, **kwargs):
    return render(request, 'admin_portal/admin_portal_home.html', {})

# needs logged in as admin required decorator
def create_user_view(request, *args, **kwargs):
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
                admin_group, created = Group.objects.get_or_create(name='Admin')
                new_user.groups.add(admin_group)
                #new_user_role = Admin(user=new_user)
            elif user_type == 'Instructor':
                instructor_group, created = Group.objects.get_or_create(name='Instructor')
                new_user.groups.add(instructor_group)
                #new_user_role = Instructor(user=new_user)
            elif user_type == 'Student':
                student_group, created = Group.objects.get_or_create(name='Student')
                new_user.groups.add(student_group)
                #new_user_role = Student(user=new_user)
            else:
                print('Error - invalid user_type, could not add user to user group.')
            # insert success message here
            return redirect('admin-home') # will want to redirect elsewhere most likely, e.g. list of users
        else:
            print(form.errors)
            return render(request, 'admin_portal/create_user.html', {'form': form})

    form = AdminCreateUserForm()
    return render(request, 'admin_portal/create_user.html', {'form': form})

