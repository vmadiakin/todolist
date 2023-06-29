from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='user-register'),
]
