from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

from .models import (
    WorkoutPlan, NutritionPlan, ProgressTracker,
    UserProfile, WorkoutLog
)
from .serializers import (
    WorkoutPlanSerializer, NutritionPlanSerializer,
    ProgressTrackerSerializer, UserProfileSerializer
)
from .ai_suggestions import get_workout_suggestion, get_nutrition_suggestion


# 🌐 Home Page View
def home(request):
    return render(request, 'exercise/index.html')


# ✅ Workout Plan API
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

    @action(detail=False, methods=['get'])
    def ai_suggestion(self, request):
        goal = request.GET.get('goal', None)
        if not goal:
            return Response({'error': 'Goal parameter is required'}, status=400)
        suggestion = get_workout_suggestion(goal) or []
        return Response({'suggestions': suggestion})


# ✅ Nutrition Plan API
class NutritionPlanViewSet(viewsets.ModelViewSet):
    queryset = NutritionPlan.objects.all()
    serializer_class = NutritionPlanSerializer

    @action(detail=False, methods=['get'])
    def ai_suggestion(self, request):
        meal_type = request.GET.get('meal_type', None)
        if not meal_type:
            return Response({'error': 'Meal type parameter is required'}, status=400)
        suggestion = get_nutrition_suggestion(meal_type) or []
        return Response({'suggestions': suggestion})


# ✅ Progress Tracker API
class ProgressTrackerViewSet(viewsets.ModelViewSet):
    queryset = ProgressTracker.objects.all()
    serializer_class = ProgressTrackerSerializer

    @action(detail=True, methods=['get'])
    def retrieve_progress(self, request, pk=None):
        progress = self.get_object()
        return Response({
            'weight': progress.weight,
            'body_fat_percentage': progress.body_fat_percentage,
            'muscle_mass': progress.muscle_mass
        })


# ✅ User Profile API
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# ✅ AI Meal Recommendation Endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meal_recommendation(request):
    meal_type = request.GET.get('meal_type', 'lunch')
    suggestion = get_nutrition_suggestion(meal_type)
    if not suggestion:
        return JsonResponse({"error": "Invalid meal type selected"}, status=400)
    return JsonResponse(suggestion)


# ✅ AI Workout Recommendation Endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workout_recommendation(request):
    goal = request.GET.get('goal', 'weight_loss')
    suggestion = get_workout_suggestion(goal)
    if not suggestion:
        return JsonResponse({"error": "Invalid workout goal"}, status=400)
    return JsonResponse(suggestion)


# ✅ AI Chatbot Endpoint
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ai_chatbot(request):
    user_message = request.data.get("message", "").lower()
    responses = {
        "hello": "Hi there! How can I assist you with your fitness goals?",
        "workout plan": "I recommend strength training and cardio. Do you want a specific plan?",
        "meal plan": "Try high-protein meals with balanced carbs and fats.",
        "bmi": "Use the calculator on our homepage to check your BMI.",
        "bye": "Goodbye! Stay fit and take care!"
    }
    bot_response = responses.get(user_message, "I'm not sure, but I can help with workouts and meals!")
    return JsonResponse({"response": bot_response})


# ✅ Workout Log POST API
class WorkoutLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            WorkoutLog.objects.create(
                user=request.user,
                exercise=data['exercise'],
                sets=data['sets'],
                reps=data['reps'],
                duration_minutes=data['duration']
            )
            return Response({"message": "Workout logged successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# ✅ Workout Progress Analysis API
class WorkoutProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            logs = WorkoutLog.objects.filter(user=request.user).order_by('-date')[:5]
            if not logs.exists():
                return Response({"suggestion": "Start logging your workouts to receive personalized progress advice!"})

            total_reps = sum(log.reps for log in logs)
            total_sets = sum(log.sets for log in logs)
            total_duration = sum(log.duration_minutes for log in logs)
            count = logs.count()

            avg_reps = total_reps / count
            avg_sets = total_sets / count
            avg_duration = total_duration / count

            suggestion = (
                f"🔥 You've been averaging {avg_sets:.1f} sets of {avg_reps:.1f} reps "
                f"per workout, with {avg_duration:.1f} minutes of effort.\n"
                "💡 Suggestion: Try adding 1 more set or increase reps by 2 next session!"
            )

            return Response({"suggestion": suggestion})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# ✅ Workout Chart Data API
class WorkoutChartDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = WorkoutLog.objects.filter(user=request.user).order_by('date')
        labels = [log.date.strftime('%b %d') for log in logs]
        reps = [log.reps for log in logs]
        sets = [log.sets for log in logs]
        duration = [log.duration_minutes for log in logs]

        return Response({
            "labels": labels,
            "reps": reps,
            "sets": sets,
            "duration": duration
        })
