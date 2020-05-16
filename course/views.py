from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from online_university.permissions import group_required
from .forms import CreateCourseForm
from .models import Course, Subject, CourseSection, CourseUnit, CourseContentFile


@group_required('Admin', 'Instructor')
def create_course_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST, request.FILES)
        print('uploaded files: ', request.FILES)
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


def my_courses_view(request, *args, **kwargs):
    if request.user.groups.filter(name='Instructor').exists():
        my_courses = Course.objects.filter(instructors=request.user)
    elif request.user.groups.filter(name='Student').exists():
        my_courses = Course.objects.filter(students=request.user)
    else:
        # TODO put a real error msg and redirect here
        return redirect('landing-page')
    # TODO: I think we might ultimately want a unique template for this one depending on if user is student or instructor
    return render(request, 'course/view_all_courses.html', {'course_list': my_courses})


def course_home_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)
    course_sections = CourseSection.objects.filter(course=course)

    course_resources = CourseContentFile.objects.filter(course=course)

    # maps course units to their parent course sections
    course_units = {}
    for section in course_sections:
        section_units = CourseUnit.objects.filter(section=section).order_by('unit_order_num')
        course_units[section] = section_units

    return render(request, 'course/course_homepage.html', {'course': course, 'course_sections': course_sections,
                                                           'course_units': course_units, 'course_resources': course_resources})


def unit_content_view(request, unit_id, *args, **kwargs):
    unit = get_object_or_404(CourseUnit, pk=unit_id)
    return render(request, 'course/unit_content.html', {'unit': unit})
