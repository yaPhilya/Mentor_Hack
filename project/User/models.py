from django.db import models
from django.contrib.auth.models import User as BaseUser
# Create your models here.

class User(BaseUser):
    location = models.CharField(max_length=30)
    
