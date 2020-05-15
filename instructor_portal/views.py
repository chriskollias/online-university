from django.shortcuts import render
from online_university.permissions import group_required

@group_required('Instructor')
def instructor_portal_home_view(request, *args, **kwargs):
    return render(request, 'instructor_portal/instructor_portal_home.html', {})

