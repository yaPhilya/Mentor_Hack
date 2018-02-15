from django.db import models
from django.forms import forms

from User.models import User


class Resume(models.Model):
    ch1 = '1'
    ch2 = '2'
    ch3 = '3'
    ch4 = '4'
    CHOICES_TYPE = ((ch1, 'I\'m a mentor'), (ch2, 'I\'m a mentee'),
                    (ch3, 'I\'ve a startup, looking for a collaborator'),
                    (ch4, 'I\'m looking for a team and a project to join'))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=CHOICES_TYPE)
    text = models.TextField(max_length=800)
    was_processed = models.BooleanField(default=False)
    text_filtered = models.TextField(max_length=600)
