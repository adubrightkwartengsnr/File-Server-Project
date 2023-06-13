from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import File


@login_required(login_url='accounts/login')
def home(request):
    return render(request, "main/home.html")


def file_view(request, *args, **kwargs):
    files = File.objects.all()
    return render(request, 'main/file_list.html', {'files': files})
