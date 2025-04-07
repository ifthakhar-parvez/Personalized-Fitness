from rest_framework import serializers
from .models import WorkoutPlan, NutritionPlan, ProgressTracker, DailyExerciseLog
from database.models import CustomUser  # ✅ Main user model

# WorkoutPlan Serializer
class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

# NutritionPlan Serializer
class NutritionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionPlan
        fields = '__all__'

# ProgressTracker Serializer
class ProgressTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressTracker
        fields = '__all__'

# ✅ CustomUser Serializer (not UserProfile)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class DailyExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyExerciseLog
        fields = ['title', 'duration_minutes', 'timestamp', 'calories_burned']
        read_only_fields = ['timestamp', 'calories_burned']

