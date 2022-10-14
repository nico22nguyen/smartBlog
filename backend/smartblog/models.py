from django.db import models

class User(models.model):
  email = models.CharField(max_length=100)
  password = models.CharField(max_length=100)