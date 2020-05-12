from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    course_code = models.CharField(max_length=8, unique=True)
    subject = models.CharField(max_length=100)
    syllabus = models.FileField(null=True)
    instructors = models.ManyToManyField(User, related_name='instructors')
    students = models.ManyToManyField(User, related_name='students')
    # optional: add start/end dates

    def __str__(self):
        return f'{self.name} ({self.course_code})'