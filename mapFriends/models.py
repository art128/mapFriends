from django.db import models
from django.contrib.auth.models import User

class Facebook(models.Model):
    user = models.OneToOneField(User)
    uid = models.CharField(max_length=255, primary_key=True)
    access_token = models.CharField(max_length=255)
    expire_token = models.CharField(max_length=255)
