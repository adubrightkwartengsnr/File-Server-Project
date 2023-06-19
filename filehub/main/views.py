from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from .models import File
from django.db import models
from django.http import HttpResponse,FileResponse
import requests
from urllib.parse import urljoin
from .forms import EmailForm


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

# def preview_file(request,file_id):
#     file_obj = File.objects.get(id=file_id)
#     file_url = file_obj.file.path
    
#     # Get the base url of the application
#     base_url = request.build_absolute_uri('/')[:-1]
    
#     # join base_url with file_url to get the absolute_file_url
#     absolute_file_url= urljoin(base_url,file_url)
#     # Get the content of the file
#     response = requests.get(absolute_file_url)
    
    
#     return HttpResponse(response.content)



def preview_file(request,file_id):
    file_obj = File.objects.get(id=file_id)
    file_path = file_obj.file.path
    response = FileResponse(open(file_path,'rb'))
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



    
