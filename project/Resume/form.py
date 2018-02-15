from django import forms
from django.db import models
from Resume.models import Resume


class ResumeCreationForm(forms.ModelForm):
    ch1 = '1'
    ch2 = '2'
    ch3 = '3'
    ch4 = '4'
    CHOICES_TYPE = ((ch1, 'I\'m a mentor'), (ch2, 'I\'m a mentee'),
                    (ch3, 'I\'ve a startup, looking for a collaborator'),
                    (ch4, 'I\'m looking for a team and a project to join'))
    type = forms.ChoiceField(choices=CHOICES_TYPE, widget=forms.RadioSelect())
    class Meta:
        model = Resume
        fields = ['type', 'text']

