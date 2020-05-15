from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from online_university.permissions import group_required
from .forms import CreateCourseForm
from .models import Course, Subject, CourseSection, CourseUnit


@group_required('Admin', 'Instructor')
def create_course_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New course has been created.")
            return redirect('all-courses')
        else:
            # TODO: handle invalid form
            print('invalid course creation form')
            print(form.errors) 
    form = CreateCourseForm()
    return render(request, 'course/create_new_course.html', {'form': form})       


def all_courses_view(request, *args, **kwargs):
    course_list = Course.objects.all()
    return render(request, 'course/view_all_courses.html', {'course_list': course_list})


def course_home_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)
    course_sections = CourseSection.objects.filter(course=course)

    # maps course units to their parent course sections
    course_units = {}
    for section in course_sections:
        section_units = CourseUnit.objects.filter(section=section).order_by('unit_order_num')
        course_units[section] = section_units

    #print(f'Course units: {course_units}')
    return render(request, 'course/course_homepage.html', {'course': course, 'course_sections': course_sections,
                                                           'course_units': course_units})
