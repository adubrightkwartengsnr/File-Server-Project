from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import File
from django.db import models
from django.http import HttpResponse
import requests
from urllib.parse import urljoin


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
    file_obj = File.objects.get(id=file_id)
    file_url = file_obj.file.url
    
    # Get the base url of the application
    base_url = request.build_absolute_uri('/')[:-1]
    
    # join base_url with file_url to get the absolute_file_url
    absolute_file_url= urljoin(base_url,file_url)
    # Get the content of the file
    response = requests.get(absolute_file_url)
    
    return HttpResponse(response.content)