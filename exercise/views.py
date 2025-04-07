from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import WorkoutPlan, NutritionPlan, ProgressTracker, WorkoutLog, DailyExerciseLog
from .serializers import WorkoutPlanSerializer, NutritionPlanSerializer, ProgressTrackerSerializer, CustomUserSerializer, DailyExerciseLogSerializer
from .ai_suggestions import get_workout_suggestion, get_nutrition_suggestion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from database.models import CustomUser
from django.conf import settings
import requests
from django.utils import timezone


CALORIE_BURN_RATES = {
    "walking": 4.0,
    "running": 10.0,
    "cycling": 8.0,
    "yoga": 3.0,
    "strength_training": 6.0,
    "jump_rope": 12.0,
    "aerobics": 7.0,
    "swimming": 9.0,
    "default": 5.0
}

def estimate_calories(exercise_title, duration_minutes):
    key = exercise_title.lower().replace(" ", "_")
    rate = CALORIE_BURN_RATES.get(key, CALORIE_BURN_RATES["default"])
    return round(rate * duration_minutes, 2)




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

    system_prompt = (
        "You are a helpful fitness assistant named SoftGrid. Always focus your answers on fitness, health, diet, gym tips, "
        "workouts, motivation, and wellness. Stay friendly and professional. Avoid topics unrelated to fitness."
    )

    # 🛠️ Clean history and ensure all items are strings
    history = request.session.get("chat_history", [])
    history = [str(h) for h in history if isinstance(h, str)]
    history.append(f"<|user|>\n{user_message}\n<|assistant|>")
    history = history[-5:]
    request.session["chat_history"] = history

    conversation = f"<|system|>\n{system_prompt}\n" + "\n".join(history)

    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
    }
    payload = {"inputs": conversation}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()
        if not isinstance(response_data, list) or "generated_text" not in response_data[0]:
            return Response({"error": "⚠️ Invalid response from Hugging Face API."}, status=500)

        generated_text = response_data[0]["generated_text"]
        reply = generated_text.split("<|assistant|>")[-1].strip()

        # ✅ Save full reply in history
        history[-1] += reply
        request.session["chat_history"] = history

        return Response({"response": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
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



# ✅ Only keep one correct version of DailyExerciseLogViewSet with calorie calculation logic
class DailyExerciseLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DailyExerciseLogSerializer

    def get_queryset(self):
        return DailyExerciseLog.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "")
        duration = serializer.validated_data.get("duration_minutes", 0)
        calories = estimate_calories(title, duration)
        serializer.save(user=self.request.user, calories_burned=calories)




# ✅ Keep UserProfileViewSet as it is
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# ✅ Daily Summary View

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_summary(request):
    today = timezone.now().date()
    logs = DailyExerciseLog.objects.filter(user=request.user, timestamp__date=today)

    total_duration = sum(log.duration_minutes for log in logs)
    total_calories = sum(log.calories_burned for log in logs)
    exercises = [log.title for log in logs]

    return Response({
        "date": str(today),
        "total_exercises": len(exercises),
        "total_duration_minutes": total_duration,
        "total_calories_burned": total_calories,
        "exercise_titles": exercises,
    })
