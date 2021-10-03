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

def transcript_text(request, past_conversation_id=None):
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

                # New
                if past_conversation_id is None:
                    job_id, conversation_id = generate_text_transcription(request, contents, doc)
                # Append
                else:
                    job_id, conversation_id = generate_text_transcription(request, contents, doc, past_conversation_id, 'append')

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

def generate_text_transcription(request, contents, doc, past_conversation_id=None, transcript_type=None):
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
    # New
    if transcript_type is None:
        conversation_object = symbl.Text.process(payload=payload, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False)
    # Append
    else:
        conversation_object = symbl.Text.append(payload=payload, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False, conversation_id=past_conversation_id)

    job_id = conversation_object.get_job_id()
    conversation_id = conversation_object.get_conversation_id()
    
    # Saving job_id and conversation_id
    doc.job_id = job_id
    doc.conversation_id = conversation_id
    
    doc.save()

    return job_id, conversation_id



def generate_audio_video_transcription(request, path, doc, media_type, past_conversation_id=None, transcript_type=None, speaker_list=None, speakers_email=None):
    app_id = request.user.app_id
    secret_id = request.user.secret_id
    
    channelMetadata = []
    diarizationSpeakerCount = 1
    # If multiple speakers are there
    if ',' in speaker_list and ',' in speakers_email:
        speakers = speaker_list.split(',')
        emails = speakers_email.split(',')
        
        # The count of speakers and emails must be same
        if len(speakers) == len(emails):
            speakers = [speaker.strip() for speaker in speakers]
            emails = [email.strip() for email in emails]
            
            diarizationSpeakerCount = len(speakers)
            speaker_count = 0
            counter = 0
            for speaker in speakers:
                speaker_count += 1
                channelMetadata.append({"channel": speaker_count, "speaker": {"name": speaker, "email": emails[counter]}})
                counter += 1
    
    # If there is a single speaker
    else:
        speaker = speaker_list.strip()
        email = speakers_email.strip()

        channelMetadata.append({"channel": 1, "speaker": {"name": speaker, "email": email}})
    
    # print(channelMetadata)

    # Audio
    if media_type == 'audio':
        # New
        if transcript_type is None:
            conversation_object = symbl.Audio.process_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False, parameters={
            'name':doc.name, 
            'detectPhrases': True, 
            'enableSpeakerDiarization': True,
            'diarizationSpeakerCount': diarizationSpeakerCount, 
            'channelMetadata': channelMetadata, })
        # Append
        else: 
            conversation_object = symbl.Audio.append_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False, parameters={
            'name':doc.name, 
            'detectPhrases': True, 
            'enableSpeakerDiarization': True,
            'diarizationSpeakerCount': diarizationSpeakerCount, 
            'channelMetadata': channelMetadata, }, conversation_id=past_conversation_id)
    # Video
    else:
        # New
        if transcript_type is None:
            conversation_object = symbl.Video.process_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False, parameters={
            'name':doc.name, 
            'detectPhrases': True, 
            'enableSpeakerDiarization': True, 
            'diarizationSpeakerCount': diarizationSpeakerCount, 
            'channelMetadata': channelMetadata, })
        # Append
        else: 
            conversation_object = symbl.Video.append_file(file_path=path, credentials={'app_id': app_id, 'app_secret': secret_id}, wait=False, parameters={
            'name':doc.name, 
            'detectPhrases': True, 
            'enableSpeakerDiarization': True, 
            'diarizationSpeakerCount': diarizationSpeakerCount, 
            'channelMetadata': channelMetadata, }, conversation_id=past_conversation_id)
        
    job_id = conversation_object.get_job_id()
    conversation_id = conversation_object.get_conversation_id()
    
    # Saving job_id and conversation_id
    doc.job_id = job_id
    doc.conversation_id = conversation_id
    
    doc.save()
    return job_id, conversation_id

# For Audio
def transcript_audio(request, past_conversation_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            request_for = request.POST.get('request')
            if request_for == "file_upload":
            
                file_name = request.POST.get('file_name', None)
                
                file = request.FILES.get('file')
                doc = Document.objects.create(file=file, name=file_name, user=request.user, media_type='audio')
                path = doc.file.path
                speakers = request.POST.get('speakers', None)
                speakers_email = request.POST.get('speakers_email', None)

                # New
                if past_conversation_id is None:
                    job_id, conversation_id = generate_audio_video_transcription(request, path, doc, 'audio', speaker_list=speakers, speakers_email=speakers_email)
                
                # Append
                else:
                    job_id, conversation_id = generate_audio_video_transcription(request, path, doc, 'audio', past_conversation_id, 'append', speaker_list=speakers, speakers_email=speakers_email)

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


# For Video
def transcript_video(request, past_conversation_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            request_for = request.POST.get('request')
            if request_for == "file_upload":
            
                file_name = request.POST.get('file_name', None)
                
                file = request.FILES.get('file')
                doc = Document.objects.create(file=file, name=file_name, user=request.user, media_type='video')
                path = doc.file.path
                speakers = request.POST.get('speakers', None)
                speakers_email = request.POST.get('speakers_email', None)
                
                # New
                if past_conversation_id is None:
                    job_id, conversation_id = generate_audio_video_transcription(request, path, doc, 'video', speaker_list=speakers, speakers_email=speakers_email)
                
                # Append
                else:
                    job_id, conversation_id = generate_audio_video_transcription(request, path, doc, 'video', past_conversation_id, 'append', speaker_list=speakers, speakers_email=speakers_email)

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
        return render(request, 'transcriptions/transcript-video.html')
    return redirect('Login')



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
    if text_response != '':
        file.write(str(text_response))
    else:
        file.write("No insights available!")
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
        extract_text = lambda responses : [response.name+'\n' for response in responses]
    
        text_response = extract_text(api_response.members)

        text_response = listToString(text_response)
        fname = os.path.join(file_path, 'members' + dt.datetime.now().strftime('%Y%m%d%H%M') + '.txt')
        file = open(fname, "w+")
        file.write(str(text_response))
        file.close()
        filenames.append(fname)

    # Zip files code

    zip_subdir = doc.name + dt.datetime.now().strftime('%Y%m%d%H%M')
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
    zip_filename = f'{doc.name}.zip'
    
    # Grab ZIP file from database, make response with correct MIME-type
    resp = HttpResponse(doc.zip_file, content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

# History

@login_required(login_url='Login')
def view_history(request, media_type=None):
    if media_type is None:
        histories = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    else: 
        histories = Document.objects.filter(user=request.user, media_type=media_type).order_by('-uploaded_at')
    context = {
        'histories': histories,
    }
    return render(request, 'history/view-history.html', context)

# Processing URL
def process_audio_video_url(request, url, file_name, media_type, transcript_type=None, past_conversation_id=None, speaker_list=None, speakers_email=None):
    app_id = request.user.app_id
    secret_id = request.user.secret_id

    channelMetadata = []
    diarizationSpeakerCount = 1
    # If multiple speakers are there
    if ',' in speaker_list and ',' in speakers_email:
        speakers = speaker_list.split(',')
        emails = speakers_email.split(',')
        
        # The count of speakers and emails must be same
        if len(speakers) == len(emails):
            speakers = [speaker.strip() for speaker in speakers]
            emails = [email.strip() for email in emails]
            
            diarizationSpeakerCount = len(speakers)
            speaker_count = 0
            counter = 0
            for speaker in speakers:
                speaker_count += 1
                channelMetadata.append({"channel": speaker_count, "speaker": {"name": speaker, "email": emails[counter]}})
                counter += 1
    
    # If there is a single speaker
    else:
        speaker = speaker_list.strip()
        email = speakers_email.strip()

        channelMetadata.append({"channel": 1, "speaker": {"name": speaker, "email": email}})
    
    # print(channelMetadata)

    payload = {
        'url': url,
        'name': file_name,
        'detectPhrases': True, 
        'confidenceThreshold': 0.6,
        'detectEntities': True,
        'enableSeparateRecognitionPerChannel': True,
        'enableSpeakerDiarization': True,
        'channelMetadata': channelMetadata,
        'diarizationSpeakerCount': str(diarizationSpeakerCount),
    }

    if media_type == 'audio url':
        # New
        if transcript_type is None:
            conversation_object = symbl.Audio.process_url(payload=payload, wait=False, 
            credentials={'app_id': app_id, 'app_secret': secret_id})

        # Append
        else:
            conversation_object = symbl.Audio.append_url(payload=payload, wait=False, 
            credentials={'app_id': app_id, 'app_secret': secret_id}, conversation_id=past_conversation_id)
    else:
        # New
        if transcript_type is None:
            conversation_object = symbl.Video.process_url(payload=payload, wait=False, 
            credentials={'app_id': app_id, 'app_secret': secret_id})

        # Append
        else:
            conversation_object = symbl.Video.append_url(payload=payload, wait=False, 
            credentials={'app_id': app_id, 'app_secret': secret_id}, conversation_id=past_conversation_id)

    conversation_id = conversation_object.get_conversation_id()                  
    job_id = conversation_object.get_job_id()                  

    doc = Document.objects.create(name=file_name, user=request.user, media_type=media_type, job_id=job_id, conversation_id=conversation_id)

    doc.save()

    return job_id, conversation_id

# For Audio URL
def transcript_audio_url(request, past_conversation_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            request_for = request.POST.get('request')
            
            if request_for == "file_upload":
                file_name = request.POST.get('file_name', None)
                url = request.POST.get('url', None)      
                speakers = request.POST.get('speakers', None)
                speakers_email = request.POST.get('speakers_email', None)
                print(speakers)
                print(speakers_email)
                # New
                if past_conversation_id is None:
                    job_id, conversation_id = process_audio_video_url(request, url, file_name, 'audio url', speaker_list=speakers, speakers_email=speakers_email)

                # Append
                else:
                    job_id, conversation_id = process_audio_video_url(request, url, file_name, 'audio url', 'append', past_conversation_id, speaker_list=speakers, speakers_email=speakers_email)
                    
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
        return render(request, 'transcriptions/transcript-audio-url.html')
    return redirect('Login')


# For Video URL
def transcript_video_url(request, past_conversation_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            request_for = request.POST.get('request')
            app_id = request.user.app_id
            secret_id = request.user.secret_id
            
            if request_for == "file_upload":
                file_name = request.POST.get('file_name', None)
                url = request.POST.get('url', None)      
                speakers = request.POST.get('speakers', None)
                speakers_email = request.POST.get('speakers_email', None)
            
                 # New
                if past_conversation_id is None:
                    job_id, conversation_id = process_audio_video_url(request, url, file_name, 'video url', speaker_list=speakers, speakers_email=speakers_email)

                # Append
                else:
                    job_id, conversation_id = process_audio_video_url(request, url, file_name, 'video url', 'append', past_conversation_id, speaker_list=speakers, speakers_email=speakers_email)

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
        return render(request, 'transcriptions/transcript-video-url.html')
    return redirect('Login')