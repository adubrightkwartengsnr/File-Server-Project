from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import File
from django.db import models
from django.http import HttpResponse,FileResponse
import requests
from urllib.parse import urljoin
from .forms import EmailForm
from django.core.mail import EmailMessage
from django.contrib import messages
import mimetypes
import os
from dotenv import load_dotenv
import pyrebase


load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "databaseURL":"",
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
    }

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()


def home(request):
    return render(request, "main/home.html")

@login_required(login_url="accounts/login/")
def file_view(request, *args, **kwargs):
    files = File.objects.all()
    return render(request, 'main/file_list.html', {'files': files})

@login_required(login_url="accounts/login/")
def search_view(request):
    query = request.GET.get('query','')
    files = File.objects.filter(models.Q(title__icontains=query)| models.Q(description__icontains=query)|
                                models.Q(file_type__icontains=query))
    context = {'files':files ,'query':query}
    return render(request, 'main/file_search.html', context)


@login_required(login_url="accounts/login/")
def preview_file(request,file_id):
    try:
        file_obj = get_object_or_404(File,id=file_id)
        file_url = storage.child(file_obj.file.name).get_url(file_obj.file_token)
        print(file_url)
        file_response = requests.get(file_url)
        # Respond with the appropriate file content and content type
        response = HttpResponse(file_response.content)
        content_type,_ = mimetypes.guess_type(file_obj.file.name)
        response['Content-Type'] = content_type
        response['Content-Disposition'] = f'inline; filename={os.path.basename(file_obj.file.name)}'
            
        return response
    except FileNotFoundError:
        return HttpResponse("File not found",status=404)
    
        

# Function for download file

@login_required(login_url="accounts/login/")
def file_download(request,file_id):
    try:
        file_obj = get_object_or_404(File,pk=file_id)
        # Get the download url and tokens
        download_url = storage.child(file_obj.file.name).get_url(file_obj.file_token)
        
        # Send a GET request to download file
        response = requests.get(download_url)
        # Determine the content type of the file
        content_type,_ = mimetypes.guess_type(file_obj.file.name)
        
       
        http_response = HttpResponse(response.content,content_type=content_type)
        http_response['Content-Disposition'] = f'attachment; filename = "{file_obj.file.name}"'
        # Increase the number of downloads
        file_obj.downloads += 1
        file_obj.save()
        return http_response
    except FileNotFoundError:
        return HttpResponse("File Not Found")
    
    
def email_form(request,file_id):
    form = EmailForm
    file = get_object_or_404(File,pk=file_id)
    context = {
        'form':form,
        'file':file
    }
    return render(request,'main/send_email.html',context)
 

@login_required(login_url="accounts/login/")
def send_email(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    if request.method == 'POST':
        form = EmailForm(request.POST) 
        if form.is_valid():
            email = EmailMessage(
                subject=form.cleaned_data['subject'],
                body=form.cleaned_data['body'],
                from_email="noreply@filehub.com",
                to=[form.cleaned_data['to']],
                headers={'From': 'File Hub <noreply@filehub.com>'}    
            )
          # Get the download URL of the file from Firebase Storage
            file_url = storage.child(file_obj.file.name).get_url(file_obj.file_token)
            
            # Download the file using requests
            response = requests.get(file_url)
            
            # Determine the content type
            content_type,_ =mimetypes.guess_type(file_obj.file.name)
            
            # Attach the file to the email
            email.attach(file_obj.title, response.content, content_type)
            
            # Send the email
            email.send()
            
            # Increase the number of emails sent from a specific file
            file_obj.emails_sent += 1
            file_obj.save()
            
            # Send success message
            messages.success(request, f'File successfully sent to {form.cleaned_data["to"]}')
            return redirect('file-list')
        else:
            form = EmailForm()
            
        return render(request, 'main/send_email.html', {'form': form})
    return HttpResponse("Invalid request")
