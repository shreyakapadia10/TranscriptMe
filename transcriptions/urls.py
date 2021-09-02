from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.transcript_text, name='TranscriptText'),
    path('audio/', views.transcript_audio, name='TranscriptAudio'),
    # path('download_files/', views.download_files, name='DownloadFiles'),
    path('download_files/<job_id>/<conversation_id>/', views.download_files, name='DownloadFiles'),
]