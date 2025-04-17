# urls.py
from django.urls import path
from .views import update_timezone, update_language

urlpatterns = [
    path('update_timezone/', update_timezone, name='update_timezone'),
    path('update_language/', update_language, name='update_language'),
]
