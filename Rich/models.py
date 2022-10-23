from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.TextField()
    users = models.TextField()
    messages = models.TextField(default='')
