from django.shortcuts import render
from online_university.permissions import group_required

@group_required('Student')
def student_portal_home_view(request, *args, **kwargs):
    return render(request, 'student_portal/student_portal_home.html', {})
    