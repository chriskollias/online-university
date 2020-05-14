from django.contrib.auth.views import LoginView
from django.urls import path
from .views import user_register_view, user_login_redirect, user_logout_view, all_users_view, user_profile_view, user_edit_view

urlpatterns = [
    path('view-profile/<int:user_id>/', user_profile_view, name='user-profile'),
    path('all-users/', all_users_view, name='all-users'),
    path('register/', user_register_view, name='user-register'),
    path('edit-profile/<int:user_id>/', user_edit_view, name='edit-profile'),
    path('login/', LoginView.as_view(template_name='users/user_login.html'), name='user-login'),
    path('user-redirect/', user_login_redirect, name='user-redirect'),
    path('logout/', user_logout_view, name='user-logout'),
]