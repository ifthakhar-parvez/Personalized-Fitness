
from django.urls import path  # type: ignore

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home Page

    path('privacy-settings/', views.settings, name='settings'),  # Settings Page
    path('sign__up/', views.signup_view, name='sign__up'),  
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('log__in/', views.login_view, name='log__in'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('api/signup/', views.signup_view, name='api_signup'),
    path('api/login/', views.login_view, name='api_login'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('questionnaire/', views.questionnaire_view, name='questionnaire'),
    path('api/questionnaire/', views.questionnaire_api, name='api_questionnaire'),
]
