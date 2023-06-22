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

def preview_file(request,file_id):
    file_obj = get_object_or_404(File,id=file_id)
    file_path = file_obj.file.path
    file_type,_ = mimetypes.guess_type(file_path)
    
    with open(file_path,'rb') as file:
        response = HttpResponse(file.read())
        response['Content-Type'] = file_type
        # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)

        
    return response

    

# Function for download file
def file_download(request,file_id):
    file_obj = get_object_or_404(File,pk=file_id)
    file_path = file_obj.file.path
    
    # Increment the number of downloads
    file_obj.downloads += 1
    file_obj.save()
    # Get the content and content type of the file
    open_file = open(file_path,'rb')
    response = FileResponse(open_file)
    # Set the content type 
    response['Content-Type'] = 'application/octet-stream'
    # Set the content-disposition
    response['Content-Disposition'] = f'attachment; filename = "{file_obj.file.name}"'
    return response

    
def email_form(request,file_id):
    form = EmailForm
    file = get_object_or_404(File,pk=file_id)
    context = {
        'form':form,
        'file':file
    }
    return render(request,'main/send_email.html',context)
 
def send_email(request,file_id):
    file_obj = get_object_or_404(File,pk=file_id)
    file_path =file_obj.file.path
    if request.method == 'POST':
        form = EmailForm(request.POST) 
        if form.is_valid():
            email = EmailMessage(
                subject = form.cleaned_data['subject'],
                body = form.cleaned_data['body'],
                from_email="noreply@filehub.com",
                to = [form.cleaned_data['to']],headers={'From':'File Hub <noreply@filehub.com>'}    
            )
            with open(file_path,'rb') as opened_file:
                # response = requests.get(file_path)
                # Determine the content type of the file being sent
                content_type = mimetypes.guess_type(file_path)[0]
                # Attach file content to the email been sent
                email.attach(file_obj.title,opened_file.read(),content_type)
            # Send the email
            email.send()
            
            # Increase the number of emails sent from a specific file
            file_obj.emails_sent += 1
            file_obj.save()
            
            # Send Success message
            messages.success(request,f'File Successfully sent to {form.cleaned_data["to"]}')
            return redirect('file-list')
        else:
            form =EmailForm()
            
        return render(request,'main/send_email.html',{'form':form})
    return HttpResponse("Invalid request") 

        
