from django.urls import path
from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view()),
    path("goal_category/list", views.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", views.GoalCategoryView.as_view()),
    path('goal/create', views.GoalCreateView.as_view()),
    path('goal/<int:pk>', views.GoalAPIView.as_view()),
    path('goal/list', views.GoalListView.as_view()),
    path('goal_comment/', views.CommentListView.as_view()),
    path('goal_comment/create/', views.CommentCreateView.as_view()),
    path('goal_comment/<int:pk>/', views.CommentAPIView.as_view()),
]
