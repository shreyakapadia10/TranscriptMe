from transcriptions.models import Document
from django.shortcuts import redirect, render
import symbl
import json
import requests
# Create your views here.

def transcript_text(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            messages = request.POST.get('messages', None)
            action_items = request.POST.get('action_items', None)
            questions = request.POST.get('questions', None)
            topics = request.POST.get('topics', None)
            follow_ups = request.POST.get('follow_ups', None)
            members = request.POST.get('members', None)

            file = request.FILES.get('file')
            doc = Document.objects.create(file=file, name=file.name)
            path = doc.file.path

            with open(path, 'r') as f:
                contents = f.read()

            generate_text_transcription(
                request, messages, action_items, questions, topics, follow_ups, members, contents)

        return render(request, 'transcriptions/transcript-text.html')
    return redirect('Login')


def generate_text_transcription(request, messages, action_items, questions, topics, follow_ups, members, contents):
    app_id = request.user.app_id
    secret_id = request.user.secret_id

    payload = {
        "confidenceThreshold": 0.6,
        "detectPhrases": True,
        "messages": [
            {
                "payload": {
                    "content": contents,
                    "contentType": "text/plain"
                },
                "from": {
                    "name": request.user.full_name(),
                    "userId": request.user.email
                }
            }
        ]
    }

    conversation_object = symbl.Text.process(payload=payload, credentials={
        'app_id': app_id, 'app_secret': secret_id})

    if messages is not None:
        print(conversation_object.get_messages())
    if topics is not None:
        print(conversation_object.get_topics())
    if follow_ups is not None:
        print(conversation_object.get_follow_ups())
    if action_items is not None:
        print(conversation_object.get_action_items())
    if questions is not None:
        print(conversation_object.get_questions())
    if members is not None:
        print(conversation_object.get_members())



# For Audio
def transcript_audio(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            messages = request.POST.get('messages', None)
            action_items = request.POST.get('action_items', None)
            questions = request.POST.get('questions', None)
            topics = request.POST.get('topics', None)
            follow_ups = request.POST.get('follow_ups', None)
            members = request.POST.get('members', None)

            file = request.FILES.get('file')
            doc = Document.objects.create(file=file, name=file.name)
            path = doc.file.path
        
            generate_audio_transcription(request, messages, action_items, questions, topics, follow_ups, members, path)

        return render(request, 'transcriptions/transcript-audio.html')
    return redirect('Login')


def generate_audio_transcription(request, messages, action_items, questions, topics, follow_ups, members, path):
    app_id = request.user.app_id
    secret_id = request.user.secret_id
    
    conversation_object = symbl.Audio.process_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id})

    if messages is not None:
        print(conversation_object.get_messages())
    if topics is not None:
        print(conversation_object.get_topics())
    if follow_ups is not None:
        print(conversation_object.get_follow_ups())
    if action_items is not None:
        print(conversation_object.get_action_items())
    if questions is not None:
        print(conversation_object.get_questions())
    if members is not None:
        print(conversation_object.get_members())
