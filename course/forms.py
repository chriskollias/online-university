from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Course, Subject, CourseSection, CourseUnit

class CreateCourseForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=250)
    course_code = forms.CharField(max_length=8)
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    syllabus = forms.FileField(required=False)
    instructors = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Instructor']), required=False)
    students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Student']), required=False)
    # optional: add start/end dates

    class Meta:
        model = Course
        fields = ['name', 'description', 'course_code', 'subject', 'syllabus', 'instructors', 'students']


class EditCourseDetailsForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=250)
    course_code = forms.CharField(max_length=8)
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = Course
        fields = ['name', 'description', 'course_code', 'subject']


class EditCourseEnrollmentForm(forms.ModelForm):
    instructors = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Instructor']), required=False)
    students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Student']), required=False)

    class Meta:
        model = Course
        fields = ['instructors', 'students']


class CreateCourseSection(forms.ModelForm):
    # should automatically select the course we're editing
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=250)
    section_order_num = forms.IntegerField() # need to handle no-duplicates

    class Meta:
        model = CourseSection
        fields = ['name', 'description', 'section_order_num']


class CreateCourseUnit(forms.ModelForm):
    section = forms.ChoiceField() # need to get list of existing sections, or will it be automatic?
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=250)
    unit_order_num = forms.IntegerField() # need to handle no-duplicates

    class Meta:
        model = CourseUnit
        fields = ['section', 'name', 'description', 'unit_order_num']