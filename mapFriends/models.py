'''
from django.db import models


class User(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField()
    Email = models.CharField()
    Password = models.CharField()
'''