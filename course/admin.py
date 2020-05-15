from django.contrib import admin
from .models import Course, Subject, CourseSection, CourseUnit, CourseContentFile

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(CourseSection)
admin.site.register(CourseUnit)
admin.site.register(CourseContentFile)

