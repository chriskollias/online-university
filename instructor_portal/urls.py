from django.urls import path
from .views import instructor_portal_home_view

urlpatterns = [
    path('', instructor_portal_home_view, name='instructor-home'),
]