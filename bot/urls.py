from django.urls import path

from . import views

urlpatterns = [
    path("verify", views.VerificationView.as_view()),
]
