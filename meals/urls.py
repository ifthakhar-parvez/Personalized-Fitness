from django.urls import path
from . import views  # Import views from the same app

urlpatterns = [
     path('', views.nutrition_index, name='Nutrition'),
     path('chatbot/', views.chatbot_response, name='chatbot'),
]