from django.db import models
from database.models import CustomUser  # ✅ Import shared UserProfile model
from django.conf import settings



# Workout Plan Model
class WorkoutPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    goal = models.CharField(max_length=100)  # e.g., 'muscle_gain', 'weight_loss'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Workout Performance Model
class WorkoutPerformance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ✅ Linked to shared UserProfile
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    duration = models.FloatField(help_text="Duration in minutes")
    difficulty = models.CharField(max_length=10, choices=[('Easy', 'Easy'), ('Moderate', 'Moderate'), ('Hard', 'Hard')])
    heart_rate = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.exercise} ({self.difficulty})"


# Nutrition Plan Model
class NutritionPlan(models.Model):
    meal_type = models.CharField(max_length=100)
    meal_name = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.meal_name


# AI-Generated Meal Plan Model
class MealPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ✅ linked to UserProfile
    meal_type = models.CharField(max_length=10, choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')])
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    meal_name = models.CharField(max_length=100)
    ingredients = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.meal_name} ({self.meal_type})"


# Progress Tracker Model
class ProgressTracker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weight = models.FloatField()
    goal_weight = models.FloatField()
    body_fat_percentage = models.FloatField()
    muscle_mass = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Progress for {self.user}"


# Workout Log Model
class WorkoutLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    duration_minutes = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.exercise} ({self.date})"
    
# models.py
class DailyExerciseLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.timestamp.date()}"
