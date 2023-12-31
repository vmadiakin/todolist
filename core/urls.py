from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserRetrieveUpdateView, ChangePasswordView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='user-register'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('profile', UserRetrieveUpdateView.as_view(), name='profile'),
    path('update_password', ChangePasswordView.as_view(), name='change-password'),
]
