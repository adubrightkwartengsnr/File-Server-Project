from django.db import models
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
import tempfile
from dotenv import load_dotenv
import os 
import pyrebase
load_dotenv()


firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "databaseURL": "",
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()
# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/',default=None)
    file_type = models.CharField(max_length=100)
    downloads = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now=True)
    file_token = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.id and self.file: #New instance of the file
            # Create temporary file on the loacal system
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file.write(self.file.read())
            tmp_file.close()
            
            # Upload the file to Firebase Storage
            firebase_file_path = f'uploads{self.file.name}'
            firebase_url=storage.child(firebase_file_path).put(tmp_file.name)
            # Set the download url 
            download_url = storage.child(firebase_url['name']).get_url(firebase_url['downloadTokens'])
            
            # Set the file url 
            self.file = firebase_file_path
             # Set the file URL and file token
            self.file_token = firebase_url['downloadTokens']
            os.remove(tmp_file.name)
    
        super().save(*args,**kwargs)
            
            
            
            
            
    

