from django.shortcuts import render

# Create your views here.
def student_portal_home_view(request, *args, **kwargs):
    return render(request, 'student_portal/student_portal_home.html', {})
    