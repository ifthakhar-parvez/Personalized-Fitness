from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercise import views  
from .views import WorkoutLogAPIView
from .views import WorkoutProgressAPIView
from .views import WorkoutChartDataAPIView
from .views import get_personalized_workout

# API router for ViewSets
router = DefaultRouter()
router.register(r'workout-plans', views.WorkoutPlanViewSet, basename="workoutplan")
router.register(r'nutrition-plans', views.NutritionPlanViewSet, basename="nutritionplan")
router.register(r'progress-trackers', views.ProgressTrackerViewSet, basename="progresstracker")
router.register(r'user-profiles', views.UserProfileViewSet, basename="userprofile")

urlpatterns = [
    path('workout_chart/', views.WorkoutChartDataAPIView.as_view(), name='workout_chart'),
    path('log_workout/', views.WorkoutLogAPIView.as_view(), name='log_workout'),
    path('workout_progress/', views.WorkoutProgressAPIView.as_view(), name='workout_progress'),
    path('ai_chatbot/', views.ai_chatbot, name='ai_chatbot'),
    path('recommend/', views.get_workout_recommendation, name='workout_recommend'),
    path('meal_recommend/', views.get_meal_recommendation, name='meal_recommend'),
    path('personalized_workout/', views.get_personalized_workout, name='personalized_workout'),
]
