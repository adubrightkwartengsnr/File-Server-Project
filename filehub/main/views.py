from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import File
from django.db import models

@login_required(login_url='accounts/login')
def home(request):
    return render(request, "main/home.html")


def file_view(request, *args, **kwargs):
    files = File.objects.all()
    return render(request, 'main/file_list.html', {'files': files})


def search_view(request):
    query = request.GET.get('query','')
    files = File.objects.filter(models.Q(title__icontains=query)| models.Q(description__icontains=query)|
                                models.Q(file_type__icontains=query))
    context = {'files':files ,'query':query}
    return render(request, 'main/file_search.html', context)
