from django.contrib import admin
from .models import File
from django import forms

# Customize django admin forms to make uploads to firebase

class FileAdminForm(forms.ModelForm):
    class Meta:
        model = File
        fields ="__all__"
        widgets = {
            "file":forms.ClearableFileInput()
        }
        
class FileAdmin(admin.ModelAdmin):
    form = FileAdminForm

admin.site.register(File,FileAdmin)

