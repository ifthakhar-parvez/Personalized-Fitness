from django.contrib import admin
from .models import WorkoutPlan, NutritionPlan, MealPlan, ProgressTracker, WorkoutLog

# WorkoutPlan Admin
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'goal', 'created_at']
    search_fields = ['name', 'goal']
    list_filter = ['goal']

# NutritionPlan Admin
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ['meal_type', 'meal_name', 'calories', 'protein', 'carbs', 'fats', 'created_at']
    search_fields = ['meal_name', 'meal_type']
    list_filter = ['meal_type']

# ProgressTracker Admin
class ProgressTrackerAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'body_fat_percentage', 'muscle_mass', 'created_at']
    search_fields = ['user__id']  # or 'user__email' if CustomUser is linked
    list_filter = ['user']

# Register only what belongs to this app
admin.site.register(WorkoutPlan, WorkoutPlanAdmin)
admin.site.register(ProgressTracker, ProgressTrackerAdmin)
admin.site.register(WorkoutLog)
