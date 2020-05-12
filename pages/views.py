from django.shortcuts import render, redirect


def landing_page_view(request, *args, **kwargs):
    # redirect to proper portal if they are already logged in
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('admin-home')
    elif user.groups.filter(name='Instructor').exists():
        return redirect('instructor-home')
    elif user.groups.filter(name='Student').exists():
        return redirect('student-home')
    return render(request, 'pages/landing-page.html', {})
