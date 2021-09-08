from django.http.response import JsonResponse
from symbl.Conversations import Conversation
from transcriptions.models import Document
from django.shortcuts import redirect, render
import symbl
from django.conf import settings
import os
import zipfile
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
import datetime as dt
from django.contrib.auth.decorators import login_required

def transcript_text(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            request_for = request.POST.get('request')
            if request_for == "file_upload":
            
                file_name = request.POST.get('file_name', None)
                
                file = request.FILES.get('file')
                doc = Document.objects.create(file=file, name=file_name, user=request.user, media_type='text')
                path = doc.file.path

                with open(path, 'r') as f:
                    contents = f.read()

                job_id, conversation_id = generate_text_transcription(request, contents, doc)

                response = {
                    'job_id': job_id,
                    'conversation_id': conversation_id,
                }

                return JsonResponse(response)
            else:
                messages = request.POST.get('messages', None)
                action_items = request.POST.get('action_items', None)
                questions = request.POST.get('questions', None)
                topics = request.POST.get('topics', None)
                follow_ups = request.POST.get('follow_ups', None)
                members = request.POST.get('members', None)
                conversation_id = request.POST.get('conversation_id')
                job_id = request.POST.get('job_id')
                doc = Document.objects.get(job_id=job_id, conversation_id=conversation_id)
                
                job_id, conversation_id = save_response(request, conversation_id, job_id, messages, topics, follow_ups, action_items, questions, members, doc)

                response = {
                    'job_id': job_id,
                    'conversation_id': conversation_id,
                }

                return JsonResponse(response)

        return render(request, 'transcriptions/transcript-text.html')
    return redirect('Login')

def generate_text_transcription(request, contents, doc):
    app_id = request.user.app_id
    secret_id = request.user.secret_id

    payload = {
        "name": doc.name,
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
        'app_id': app_id, 'app_secret': secret_id}, wait=False)
    job_id = conversation_object.get_job_id()
    conversation_id = conversation_object.get_conversation_id()
    
    # Saving job_id and conversation_id
    doc.job_id = job_id
    doc.conversation_id = conversation_id
    
    doc.save()

    return job_id, conversation_id

# For Audio
def transcript_audio(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            request_for = request.POST.get('request')
            if request_for == "file_upload":
            
                file_name = request.POST.get('file_name', None)
                
                file = request.FILES.get('file')
                doc = Document.objects.create(file=file, name=file_name, user=request.user, media_type='audio')
                path = doc.file.path

                job_id, conversation_id = generate_audio_transcription(request, path, doc)

                response = {
                    'job_id': job_id,
                    'conversation_id': conversation_id,
                }

                return JsonResponse(response)
            else:
                messages = request.POST.get('messages', None)
                action_items = request.POST.get('action_items', None)
                questions = request.POST.get('questions', None)
                topics = request.POST.get('topics', None)
                follow_ups = request.POST.get('follow_ups', None)
                members = request.POST.get('members', None)
                conversation_id = request.POST.get('conversation_id')
                job_id = request.POST.get('job_id')
                doc = Document.objects.get(job_id=job_id, conversation_id=conversation_id)
                
                job_id, conversation_id = save_response(request, conversation_id, job_id, messages, topics, follow_ups, action_items, questions, members, doc)

                response = {
                    'job_id': job_id,
                    'conversation_id': conversation_id,
                }

                return JsonResponse(response)
        return render(request, 'transcriptions/transcript-audio.html')
    return redirect('Login')


def generate_audio_transcription(request, path, doc):
    app_id = request.user.app_id
    secret_id = request.user.secret_id
    
    conversation_object = symbl.Audio.process_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False, parameters={
    'name':doc.name, 
    'detectPhrases': True, 
    'enableSpeakerDiarization': True, 
    'diarizationSpeakerCount': 3, })
    
    job_id = conversation_object.get_job_id()
    conversation_id = conversation_object.get_conversation_id()
    
    # Saving job_id and conversation_id
    doc.job_id = job_id
    doc.conversation_id = conversation_id
    
    doc.save()
    return job_id, conversation_id

# listToString function
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 


# To process response
def process_response(response, file_name):
    extract_text = lambda responses : [response.text+'\n' for response in responses]
    
    text_response = extract_text(response)

    text_response = listToString(text_response)
    file = open(file_name, "w+")
    file.write(str(text_response))
    file.close()


# to save response to file
def save_response(request, conversation_id, job_id, messages, topics, follow_ups, action_items, questions, members, doc):

    filenames = []
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, 'temp')
    app_id = request.user.app_id
    secret_id = request.user.secret_id

    conversation_obj = Conversation(conversation_id=conversation_id, job_id=job_id, credentials={'app_id':app_id, 'app_secret':secret_id})
    
    while conversation_obj.get_job_status() != "completed":
        pass

    if messages is not None:      
        #To get the message from the conversation

        api_response = symbl.Conversations.get_messages(conversation_id=conversation_id)
        file = os.path.join(file_path, 'messages' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.messages, file)

        filenames.append(file)

    if topics is not None:
        #To get the topics from the conversation

        api_response = symbl.Conversations.get_topics(conversation_id=conversation_id)
        file = os.path.join(file_path,'topics' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.topics, file)

        filenames.append(file)

    if follow_ups is not None:
        #To get the topics from the conversation
        
        api_response = symbl.Conversations.get_follow_ups(conversation_id=conversation_id)
        file = os.path.join(file_path, 'follow_ups' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.follow_ups, file)

        filenames.append(file)


    if action_items is not None:
        #To get the topics from the conversation
        
        api_response = symbl.Conversations.get_action_items(conversation_id=conversation_id)
        file = os.path.join(file_path, 'action_items' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.action_items, file)

        filenames.append(file)


    if questions is not None:
        #To get the topics from the conversation
        
        api_response = symbl.Conversations.get_questions(conversation_id=conversation_id)
        file = os.path.join(file_path,'questions' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.questions, file)

        filenames.append(file)


    if members is not None:
        #To get the topics from the conversation
        
        api_response = symbl.Conversations.get_members(conversation_id=conversation_id)
        extract_text = lambda responses : [response.name+" - "+response.email+'\n' for response in responses]
    
        text_response = extract_text(api_response.members)

        text_response = listToString(text_response)
        fname = os.path.join(file_path, 'members' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        file = open(fname, "w+")
        file.write(str(text_response))
        file.close()
        filenames.append(fname)

    # Zip files code

    zip_subdir = "transcriptions" + dt.datetime.now().strftime('%Y%m%d%H%M')
    zip_filename = "%s.zip" % zip_subdir
    # Open BytesIO to grab in-memory ZIP contents
    b = BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(b, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        # Add file, at correct path
        zf.write(fpath, zip_path)
        
        
    # Must close zip for all contents to be written
    zf.close()

    b.seek(0)
    # To store it we can use a InMemoryUploadedFile
    inMemoryZipFile = InMemoryUploadedFile(b, None, zip_filename, 'application/zip', b.__sizeof__(), None)

    # saving document
    
    doc.zip_file = inMemoryZipFile
    doc.save()
    for file in filenames:
        os.remove(file)
    return job_id, conversation_id



# To download files
def download_files(request, job_id, conversation_id):
    doc = Document.objects.get(job_id=job_id, conversation_id=conversation_id)
    zip_filename = 'transcriptions.zip'
    
    # Grab ZIP file from database, make response with correct MIME-type
    resp = HttpResponse(doc.zip_file, content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

# History

@login_required(login_url='Login')
def view_history(request):
    histories = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {
        'histories': histories,
    }
    return render(request, 'history/view-history.html', context)