from django.urls import path
from .views import all_courses_view, create_course_view, course_home_view, unit_content_view, my_courses_view, \
    edit_course_content_view, edit_course_details_view, edit_course_enrollment_view

urlpatterns = [
    path('all-courses/', all_courses_view, name='all-courses'),
    path('my-courses/', my_courses_view, name='my-courses'),
    path('create-new-course/', create_course_view, name='create-course'),
    path('course-home/<int:course_id>/', course_home_view, name='course-home'),
    path('view-unit/<int:unit_id>/', unit_content_view, name='unit-content'),
    path('edit-course-details/<int:course_id>', edit_course_details_view, name='edit-course-details'),
    path('edit-course-content/<int:course_id>', edit_course_content_view, name='edit-course-content'),
    path('edit-course-enrollment/<int:course_id>', edit_course_enrollment_view, name='edit-course-enrollment'),
]