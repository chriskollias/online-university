from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

class Course(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    course_code = models.CharField(max_length=8, unique=True)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL) # how would I do SET_DEFAULT instead?
    syllabus = models.FileField(null=True)
    instructors = models.ManyToManyField(User, related_name='instructors')
    students = models.ManyToManyField(User, related_name='students')
    # optional: add start/end dates

    def __str__(self):
        return f'{self.name} ({self.course_code})'


 