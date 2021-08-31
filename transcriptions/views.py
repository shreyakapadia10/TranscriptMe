from transcriptions.models import Document
from django.shortcuts import redirect, render
import symbl
import json
# Create your views here.

# generating token
# def generate_token(appId, appSecret):
#     url = "https://api.symbl.ai/oauth2/token:generate"
#     payload = {
#         "type": "application",
#         "appId": appId,
#         "appSecret": appSecret
#     }
#     headers = {
#         'Content-Type': 'application/json'
#     }

#     responses = {
#         400: 'Bad Request! Please refer docs for correct input fields.',
#         401: 'Unauthorized. Please generate a new access token.',
#         404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
#         429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
#         500: 'Something went wrong! Please contact support@symbl.ai'
#     }

#     response = requests.request(
#         "POST", url, headers=headers, data=json.dumps(payload))

#     if response.status_code == 200:
#         # Successful API execution
#         # print("accessToken => " + response.json()['accessToken'])  # accessToken of the user
#         # print("expiresIn => " + str(response.json()['expiresIn']))  # Expiry time in accessToken
#         pass
#     elif response.status_code in responses.keys():
#         # Expected error occurred
#         print(responses[response.status_code], response.text)
#     else:
#         print("Unexpected error occurred. Please contact support@symbl.ai" +
#               ", Debug Message => " + str(response.text))

#     return response.json()['accessToken']


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
    # access_token = generate_token(app_id, secret_id)
    # url = "https://api.symbl.ai/v1/process/text"

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

        with open('messages.txt', 'w') as f:
            json.dump(conversation_object.get_messages(), f)
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
