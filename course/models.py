from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'

class Course(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    course_code = models.CharField(max_length=8, unique=True)
    subject = models.ManyToManyField(Subject) # how would I do SET_DEFAULT instead
    syllabus = models.FileField(upload_to='uploaded_course_syllabi/', null=True)
    instructors = models.ManyToManyField(User, related_name='instructors')
    students = models.ManyToManyField(User, related_name='students')
    # optional: add start/end dates

    def __str__(self):
        return f'{self.name} ({self.course_code})'


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    section_order_num = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.course.name} - {self.section_order_num}) {self.name}'

# this should probably also be directly connected to the Course model, not just CourseSection
class CourseUnit(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    unit_order_num = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.section.course.name}: {self.section.name} - {self.unit_order_num}) {self.name}'


class CourseContentFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    unit = models.ForeignKey(CourseUnit, null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded_course_content/')
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'