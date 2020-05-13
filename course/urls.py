from django.urls import path
from .views import all_courses_view, create_course_view, course_home_view

urlpatterns = [
    path('all-courses/', all_courses_view, name='all-courses'),
    path('create-new-course/', create_course_view, name='create-course'),
    path('course-home/<int:course_id>/', course_home_view, name='course-home'),
]