from django.urls import path

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view()),
    path("goal_category/list", views.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", views.GoalCategoryView.as_view()),
    path('goal/create', views.GoalCreateView.as_view()),
    path('goal/<int:pk>', views.GoalReadView.as_view()),
    path('goal/<int:pk>', views.GoalUpdateView.as_view()),
    path('goal/<int:pk>', views.GoalDeleteView.as_view()),
    path('goal/list', views.GoalListView.as_view()),
]
