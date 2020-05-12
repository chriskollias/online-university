from django.urls import path
from .views import *

urlpatterns = [
    path('', student_portal_home_view, name='student-home'),
]