from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.home,name="home"),
    path("file-list/",views.file_view,name="file-list"),
    path("search/",views.search_view,name="search"),
    path("file-list/<int:file_id>/preview/",views.preview_file,name='file-preview'),
    path("file-list/<int:file_id>/",views.file_download,name='file-download'),
    path("email-form/<int:file_id>/",views.email_form,name='email-form'),
    path("send_email/<int:file_id>",views.send_email,name='send-email')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)