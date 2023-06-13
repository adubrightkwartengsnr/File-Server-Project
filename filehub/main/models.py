from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/',default=None)
    file_type = models.CharField(max_length=100)
    downloads = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

