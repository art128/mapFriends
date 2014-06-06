from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=255)
    
    def __unicode__(self):
    	return self.user.username
