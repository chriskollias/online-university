from django.urls import path
from .views import *

urlpatterns = [
    path('create-user/', create_user_view, name='create-user'),
    path('', admin_portal_home_view, name='admin-home'),
]