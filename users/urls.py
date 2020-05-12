from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', user_register_view, name='user-register'),
    path('login/', LoginView.as_view(template_name='users/user_login.html'), name='user-login'),
    path('user-redirect/', user_login_redirect, name='user-redirect'),
    path('logout/', user_logout_view, name='user-logout'),
]