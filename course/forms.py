from django import forms
from .models import Course
from django.contrib.auth.models import User

class CreateCourseForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=250)
    course_code = forms.CharField(max_length=8)
    subject = forms.ChoiceField(required=False)
    syllabus = forms.FileField(required=False)
    instructors = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Instructor']), required=False)
    students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in=['Student']), required=False)
    # optional: add start/end dates

    class Meta:
        model = Course
        fields = ['name', 'description', 'course_code', 'subject', 'syllabus', 'instructors', 'students']