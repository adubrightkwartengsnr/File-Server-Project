from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.username
