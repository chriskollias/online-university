from django.shortcuts import render

# Create your views here.
def instructor_portal_home_view(request, *args, **kwargs):
    return render(request, 'instructor_portal/instructor_portal_home.html', {})
