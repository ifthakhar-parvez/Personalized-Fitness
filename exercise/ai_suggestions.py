import random

def get_workout_suggestion(goal):
    workout_plans = {
        "muscle_gain": [
            {"exercise": "Bench Press", "sets": 4, "reps": 10, "intensity": "High"},
            {"exercise": "Squats", "sets": 4, "reps": 12, "intensity": "High"},
            {"exercise": "Deadlifts", "sets": 3, "reps": 8, "intensity": "Very High"},
        ],
        "weight_loss": [
            {"exercise": "Running", "sets": 1, "reps": 30, "intensity": "Medium"},
            {"exercise": "Jump Rope", "sets": 3, "reps": 60, "intensity": "Medium"},
            {"exercise": "Cycling", "sets": 1, "reps": 40, "intensity": "Medium"},
        ],
        "maintain": [
            {"exercise": "Yoga", "sets": 1, "reps": 45, "intensity": "Low"},
            {"exercise": "Swimming", "sets": 3, "reps": 20, "intensity": "Medium"},
            {"exercise": "Full-body Strength", "sets": 2, "reps": 12, "intensity": "Moderate"},
        ]
    }

    # Ensure structured response
    return random.choice(workout_plans.get(goal, [
        {"exercise": "Not Available", "sets": "N/A", "reps": "N/A", "intensity": "N/A"}
    ]))


def get_nutrition_suggestion(meal_type):
    nutrition_plans = {
        "breakfast": [
            {"meal": "Oatmeal with fruits and nuts", "calories": 350, "protein": 10, "carbs": 45, "fats": 12},
            {"meal": "Egg whites with whole-wheat toast", "calories": 250, "protein": 20, "carbs": 30, "fats": 5},
            {"meal": "Greek yogurt with honey and seeds", "calories": 200, "protein": 18, "carbs": 25, "fats": 8}
        ],
        "lunch": [
            {"meal": "Grilled chicken with brown rice and vegetables", "calories": 450, "protein": 40, "carbs": 50, "fats": 10},
            {"meal": "Quinoa salad with chickpeas and avocado", "calories": 400, "protein": 20, "carbs": 55, "fats": 15},
            {"meal": "Salmon with steamed broccoli and sweet potato", "calories": 500, "protein": 45, "carbs": 60, "fats": 12}
        ],
        "dinner": [
            {"meal": "Baked fish with quinoa and asparagus", "calories": 420, "protein": 35, "carbs": 40, "fats": 15},
            {"meal": "Tofu stir-fry with mixed vegetables", "calories": 350, "protein": 25, "carbs": 50, "fats": 12},
            {"meal": "Lean beef with mashed sweet potatoes", "calories": 480, "protein": 50, "carbs": 55, "fats": 14}
        ]
    }

    # ✅ Ensure the meal suggestion changes dynamically
    return random.choice(nutrition_plans.get(meal_type, [{"meal": "Not Available", "calories": 0, "protein": 0, "carbs": 0, "fats": 0}]))


def get_progress_percentage(current_weight, goal_weight):
    if goal_weight <= 0 or current_weight <= 0:
        return None

    progress = ((goal_weight - current_weight) / goal_weight) * 100
    return round(progress, 2)
