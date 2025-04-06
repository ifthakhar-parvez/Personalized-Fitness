from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import WorkoutPlan, NutritionPlan, ProgressTracker, WorkoutLog
from .serializers import WorkoutPlanSerializer, NutritionPlanSerializer, ProgressTrackerSerializer, CustomUserSerializer
from .ai_suggestions import get_workout_suggestion, get_nutrition_suggestion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from database.models import CustomUser
from django.conf import settings
import requests


def home(request):
    return render(request, 'exercise/index.html')


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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_workout_recommendation(request):
    goal = request.GET.get('goal', 'weight_loss')
    suggestion = get_workout_suggestion(goal)
    if not suggestion:
        return JsonResponse({"error": "Invalid workout goal"}, status=400)
    return JsonResponse(suggestion)


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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_meal_recommendation(request):
    meal_type = request.GET.get('meal_type', 'lunch')
    suggestion = get_nutrition_suggestion(meal_type)
    if not suggestion:
        return JsonResponse({"error": "Invalid meal type selected"}, status=400)
    return JsonResponse(suggestion)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ai_chatbot(request):
    user_message = request.data.get("message", "")
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": f"<|user|>\n{user_message}\n<|assistant|>"
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        generated_text = response.json()[0].get("generated_text", "")
        reply = generated_text.split("<|assistant|>")[-1].strip()
        return Response({"response": reply})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


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


class WorkoutLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            workout = WorkoutLog.objects.create(
                user=request.user,
                exercise=data['exercise'],
                sets=data['sets'],
                reps=data['reps'],
                duration_minutes=data['duration']
            )
            return Response({"message": "Workout logged successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


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


class WorkoutChartDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = WorkoutLog.objects.filter(user=request.user).order_by('date')
        labels = [f"{log.exercise} ({log.date.strftime('%b %d')})" for log in logs]
        reps = [log.reps for log in logs]
        sets = [log.sets for log in logs]
        duration = [log.duration_minutes for log in logs]
        return Response({
            "labels": labels,
            "reps": reps,
            "sets": sets,
            "duration": duration
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personalized_workout(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        goal = getattr(user, 'goal', 'maintain')
        level = getattr(user, 'fitness_level', 'beginner')
        plans = {
            ('weight_loss', 'beginner'): "Try 20 mins cardio + bodyweight exercises.",
            ('weight_loss', 'intermediate'): "Include HIIT sessions + light weights.",
            ('weight_loss', 'advanced'): "High-intensity circuits with progressive overload.",
            ('muscle_gain', 'beginner'): "Focus on compound lifts: 3 sets x 10 reps.",
            ('muscle_gain', 'intermediate'): "Split workouts (push/pull/legs) 4x a week.",
            ('muscle_gain', 'advanced'): "Heavy lifting with periodization techniques.",
            ('maintain', 'beginner'): "Light full-body workouts 3x a week.",
            ('maintain', 'intermediate'): "3–4 sessions mixing strength & cardio.",
            ('maintain', 'advanced'): "Functional training + deload weeks."
        }
        key = (goal, level)
        plan = plans.get(key, "No personalized plan available.")
        return Response({"plan": plan})
    except CustomUser.DoesNotExist:
        return Response({"error": "User profile not found."}, status=404)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
