from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_register_view, name='user-register'),
    path('create-user/', admin_create_user_view, name='create-user'),
]