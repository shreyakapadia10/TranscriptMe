from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.transcript_text, name='TranscriptText'),
    path('text/append/<past_conversation_id>/', views.transcript_text, name='TranscriptTextAppend'),

    path('audio/', views.transcript_audio, name='TranscriptAudio'),
    path('audio/append/<past_conversation_id>/', views.transcript_audio, name='TranscriptAudioAppend'),
    
    path('audio/url/', views.transcript_audio_url, name='TranscriptAudioURL'),
    path('audio/url/append/<past_conversation_id>/', views.transcript_audio_url, name='TranscriptAudioURLAppend'),

    path('video/', views.transcript_video, name='TranscriptVideo'),
    path('video/append/<past_conversation_id>/', views.transcript_video, name='TranscriptVideoAppend'),

    path('video/url/', views.transcript_video_url, name='TranscriptVideoURL'),
    path('video/url/append/<past_conversation_id>/', views.transcript_video_url, name='TranscriptVideoURLAppend'),


    path('download_files/<conversation_id>/<job_id>/', views.download_files, name='DownloadFiles'),
    path('download_files/<conversation_id>/', views.download_files, name='DownloadFiles'),
    
    path('history/', views.view_history, name='ViewHistory'),
    path('history/<media_type>/', views.view_history, name='ViewHistoryByMedia'),

    path('zoom-call/', views.transcript_zoom_call, name='TranscriptZoomCall'),
    path('google-meet/', views.transcript_google_meet, name='TranscriptGoogleMeet'),
]