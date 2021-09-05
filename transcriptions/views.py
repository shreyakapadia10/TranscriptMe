from django.http.response import JsonResponse
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
            file_name = request.POST.get('file_name', None)
            messages = request.POST.get('messages', None)
            action_items = request.POST.get('action_items', None)
            questions = request.POST.get('questions', None)
            topics = request.POST.get('topics', None)
            follow_ups = request.POST.get('follow_ups', None)
            members = request.POST.get('members', None)
            print(messages)
            file = request.FILES.get('file')
            doc = Document.objects.create(file=file, name=file_name, user=request.user, media_type='text')
            path = doc.file.path

            with open(path, 'r') as f:
                contents = f.read()

            job_id, conversation_id = generate_text_transcription(request, messages, action_items, questions, topics, follow_ups, members, contents, doc)

            response = {
                'job_id': job_id,
                'conversation_id': conversation_id,
            }

            return JsonResponse(response)

        return render(request, 'transcriptions/transcript-text.html')
    return redirect('Login')


def generate_text_transcription(request, messages, action_items, questions, topics, follow_ups, members, contents, doc):
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

    job_id, conversation_id = save_response(request, conversation_object, messages, topics, follow_ups, action_items, questions, members, doc)

    return job_id, conversation_id

# For Audio
def transcript_audio(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            file_name = request.POST.get('file_name', None)
            messages = request.POST.get('messages', None)
            action_items = request.POST.get('action_items', None)
            questions = request.POST.get('questions', None)
            topics = request.POST.get('topics', None)
            follow_ups = request.POST.get('follow_ups', None)
            members = request.POST.get('members', None)
            if messages == 'messages': messages = None
            if action_items == 'action_items': action_items = None
            if questions == 'questions': questions = None
            if topics == 'topics': topics = None
            if follow_ups == 'follow_ups': follow_ups = None
            if members == 'members': members = None
            file = request.FILES.get('file')
            doc = Document.objects.create(file=file, name=file_name, user=request.user, media_type='audio')
            path = doc.file.path
        
            job_id, conversation_id = generate_audio_transcription(request, messages, action_items, questions, topics, follow_ups, members, path, doc)
            response = {
                'job_id': job_id,
                'conversation_id': conversation_id,
            }
            return JsonResponse(response)
        return render(request, 'transcriptions/transcript-audio.html')
    return redirect('Login')


def generate_audio_transcription(request, messages, action_items, questions, topics, follow_ups, members, path, doc):
    app_id = request.user.app_id
    secret_id = request.user.secret_id
    
    conversation_object = symbl.Audio.process_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id})

    job_id, conversation_id = save_response(request, conversation_object, messages, topics, follow_ups, action_items, questions, members, doc)
    
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
def save_response(request, conversation_object, messages, topics, follow_ups, action_items, questions, members, doc):

    filenames = []
    media_path = settings.MEDIA_ROOT
    file_path = os.path.join(media_path, 'temp')
    job_id = conversation_object.get_job_id()
    conversation_id = conversation_object.get_conversation_id()

    if messages is not None:
        # print(conversation_object.get_messages())
        
        #To get the message from the conversation
        api_response = conversation_object.get_messages()
        file = os.path.join(file_path, 'messages' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.messages, file)

        filenames.append(file)

    if topics is not None:
        # print(conversation_object.get_topics())
        
        #To get the topics from the conversation
        api_response = conversation_object.get_topics()
        file = os.path.join(file_path,'topics' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.topics, file)

        filenames.append(file)

    if follow_ups is not None:
        # print(conversation_object.get_follow_ups())
       
        #To get the topics from the conversation
        api_response = conversation_object.get_follow_ups()
        file = os.path.join(file_path, 'follow_ups' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.follow_ups, file)

        filenames.append(file)


    if action_items is not None:
        # print(conversation_object.get_action_items())

        #To get the topics from the conversation
        api_response = conversation_object.get_action_items()
        file = os.path.join(file_path, 'action_items' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.action_items, file)

        filenames.append(file)


    if questions is not None:
        # print(conversation_object.get_questions())
        
        #To get the topics from the conversation
        api_response = conversation_object.get_questions()
        file = os.path.join(file_path,'questions' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        process_response(api_response.questions, file)

        filenames.append(file)


    if members is not None:
        # print(conversation_object.get_members())
         
        #To get the topics from the conversation
        api_response = conversation_object.get_members()
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
    doc.job_id = job_id
    doc.conversation_id = conversation_id
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