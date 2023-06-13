from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.home,name="home"),
    path("file-list/",views.file_view,name="file-list")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)