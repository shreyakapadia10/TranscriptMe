from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.transcript_text, name='TranscriptText'),
    path('text/append/<past_conversation_id>/', views.transcript_text, name='TranscriptTextAppend'),
    path('audio/', views.transcript_audio, name='TranscriptAudio'),
    path('download_files/<job_id>/<conversation_id>/', views.download_files, name='DownloadFiles'),
    
    path('history/', views.view_history, name='ViewHistory'),
]