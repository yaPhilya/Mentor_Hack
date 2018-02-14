from django import forms
from django.db import models
from Resume.models import Resume


class ResumeCreationForm(forms.ModelForm):
    ch1 = '1'
    ch2 = '2'
    ch3 = '3'
    CHOICES_TYPE = ((ch1, 'Я ментор'), (ch2, 'Я ученик'), (ch3, 'У меня есть стартап, ищу сокомандника'))
    type = forms.ChoiceField(choices=CHOICES_TYPE, widget=forms.RadioSelect())
    class Meta:
        model = Resume
        fields = ['type', 'text']

