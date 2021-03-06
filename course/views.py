from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from online_university.permissions import group_required
from .forms import CreateCourseForm, EditCourseDetailsForm, EditCourseEnrollmentForm
from .models import Course, Subject, CourseSection, CourseUnit, CourseContentFile
from .utils import map_course_units


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

    # check if user is a student who is enrolled in this course
    enrolled_student = False
    if request.user.groups.filter(name='Student').exists():
        if course.students.filter(pk=request.user.pk).exists():
            enrolled_student = True

    course_units = map_course_units(course_sections)

    return render(request, 'course/course_homepage.html', {'course': course, 'course_sections': course_sections,
                'course_units': course_units, 'course_resources': course_resources, 'enrolled_student': enrolled_student})


def unit_content_view(request, unit_id, *args, **kwargs):
    unit = get_object_or_404(CourseUnit, pk=unit_id)
    return render(request, 'course/unit_content.html', {'unit': unit})


@group_required('Admin', 'Instructor')
def edit_course_details_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)

    if not (request.user.groups.filter(name='Admin').exists() or course.instructors.filter(pk=request.user.pk).exists()):
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


@group_required('Admin', 'Instructor')
def edit_course_content_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)
    course_sections = CourseSection.objects.filter(course=course)
    course_resources = CourseContentFile.objects.filter(course=course)
    course_units = map_course_units(course_sections)

    if not (request.user.groups.filter(name='Admin').exists() or course.instructors.filter(pk=request.user.pk).exists()):
        messages.warning(request, 'You do not have permission to view that page.')
        return redirect('landing-page')

    return render(request, 'course/edit_course_content.html', {'course': course, 'course_sections': course_sections,
                'course_units': course_units, 'course_resources': course_resources,})


@group_required('Admin')
def edit_course_enrollment_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)

    if not (request.user.groups.filter(name='Admin').exists() or course.instructors.filter(pk=request.user.pk).exists()):
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


def enroll_student_view(request, course_id, student_id, *args, **kwargs):
    '''
    enroll a student in a course
    '''
    course = get_object_or_404(Course, pk=course_id)
    student = get_object_or_404(User, pk=student_id)

    if not student.groups.filter(name='Student').exists():
        messages.warning(request, 'User is not a student and thus cannot be enrolled in this course.')
        return redirect(reverse('course-home'), kwargs={'course_id': course_id})

    if course.students.filter(pk=student_id).exists():
        if request.user.pk == student_id:
            messages.warning(request, 'You are already enrolled in this course.')
        else:
            messages.warning(request, 'Student is already enrolled in this course.')
        return redirect(reverse('course-home', kwargs={'course_id': course_id}))

    course.students.add(student)
    if request.user.pk == student_id:
        messages.success(request, 'You have successfully enrolled in this course.')
    else:
        messages.success(request, f'{student.first_name} {student.last_name} has been successfully enrolled in this course.')
    return redirect(reverse('course-home', kwargs={'course_id': course_id}))

@group_required('Admin', 'Instructor')
def create_course_section_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course/create_course_section.html', {'course': course})

@group_required('Admin', 'Instructor')
def create_course_unit_view(request, course_id, *args, **kwargs):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course/create_course_unit.html', {'course': course})
