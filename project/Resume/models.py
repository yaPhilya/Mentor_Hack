from django.db import models
from django.forms import forms

from User.models import User


class Resume(models.Model):
    ch1 = '1'
    ch2 = '2'
    ch3 = '3'
    CHOICES_TYPE = ((ch1, 'Я ментор'), (ch2, 'Я ученик'), (ch3, 'У меня есть стартап, ищу сокомандника'))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=CHOICES_TYPE)
    text = models.CharField(max_length=400)
