from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from online_university.permissions import group_required
from .forms import CreateCourseForm, EditCourseDetailsForm, EditCourseEnrollmentForm
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


def edit_course_details_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)

    if not (request.user.groups.filter(name='Admin').exists() or request.user.pk in course.instructors):
        messages.warning(request, 'You do not have permission to view that page.')
        return redirect('landing-page')

    if request.method == 'POST':
        form = EditCourseDetailsForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course details have been successfully updated.')
            return redirect('all-courses')
        else:
            # TODO: real error handling here
            print(form.errors)

    form = EditCourseDetailsForm(instance=course)
    return render(request, 'course/edit_course_details.html', {'form': form})


def edit_course_content_view(request, course_id, *args, **kwargs):
    return render(request, 'course/edit_course_content.html', {})


def edit_course_enrollment_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)

    if not (request.user.groups.filter(name='Admin').exists() or request.user.pk in course.instructors):
        messages.warning(request, 'You do not have permission to view that page.')
        return redirect('landing-page')

    if request.method == 'POST':
        form = EditCourseEnrollmentForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course enrollment has been successfully updated.')
            return redirect('all-courses')
        else:
            # TODO: real error handling here
            print(form.errors)

    form = EditCourseEnrollmentForm(instance=course)
    return render(request, 'course/edit_course_enrollment.html', {'form': form})
