from django.urls import path
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
