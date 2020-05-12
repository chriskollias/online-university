from django import forms
from .models import Course

class CreateCourseForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=250)
    course_code = forms.CharField(max_length=8)
    subject = forms.ChoiceField(required=False)
    syllabus = forms.FileField(required=False)
    instructors = forms.ChoiceField(required=False)
    students = forms.ChoiceField(required=False)
    # optional: add start/end dates

    class Meta:
        model = Course
        fields = ['name', 'description', 'course_code', 'subject', 'syllabus', 'instructors', 'students']