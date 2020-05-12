from django.urls import path
from .views import *

urlpatterns = [
    path('', instructor_portal_home_view, name='instructor-home')
]