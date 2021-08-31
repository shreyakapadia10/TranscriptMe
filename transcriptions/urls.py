from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.transcript_text, name='TranscriptText'),
]