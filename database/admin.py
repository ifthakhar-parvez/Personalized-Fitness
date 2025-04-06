from django.contrib import admin
from .models import CustomUser, UserQuestionnaire, UserSession

admin.site.register(CustomUser)
admin.site.register(UserQuestionnaire)
admin.site.register(UserSession)
