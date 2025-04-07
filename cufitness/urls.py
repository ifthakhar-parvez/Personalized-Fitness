from django.contrib import admin
from django.urls import path, include
from exercise import views
from rest_framework.routers import DefaultRouter
from exercise.views import DailyExerciseLogViewSet, daily_summary

router = DefaultRouter()
router.register(r'workout-plans', views.WorkoutPlanViewSet)
router.register(r'nutrition-plans', views.NutritionPlanViewSet)
router.register(r'progress-trackers', views.ProgressTrackerViewSet)
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'daily_exercises', DailyExerciseLogViewSet, basename='daily_exercises')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('explore/', include('allapps.urls')),
    path('nutrition/', include('meals.urls')),
    path('fitness/', views.home, name='fitness-home'),
    path('api/', include(router.urls)),
    path('api/', include('exercise.urls')),
    path('workout/', include('exercise.urls')),
    path('meal/', include('exercise.urls')),
    path('api/daily-summary/', daily_summary, name='daily-summary'),
]
