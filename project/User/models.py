# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, AbstractUser
#
# class User(AbstractUser):
#     austr = 'AUS'
#     rus = 'RUS'
#     usa = 'USA'
#     mex = 'MEX'
#     CHOISES_LOCATION = ((austr, 'Australia'), (rus, 'Russia'), (usa, 'USA'), (mex, 'Mexico'))
#     location = models.CharField(max_length=3, choices=CHOISES_LOCATION, default=usa)
#     username = models.CharField(max_length=30)
#     password = models.CharField(max_length=20)



from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django import forms


# class User(AbstractBaseUser, PermissionsMixin):
#     austr = 'AUS'
#     rus = 'RUS'
#     usa = 'USA'
#     mex = 'MEX'
#     CHOISES_LOCATION = ((austr, 'Australia'), (rus, 'Russia'), (usa, 'USA'), (mex, 'Mexico'))
#     location = models.CharField(max_length=3, choices=CHOISES_LOCATION, default=usa)
#     username = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=20)
#     skills = models.CharField(max_length=400)
#
#     # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, required=False)
#
#     # objects = UserManager()
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#
#     def get_full_name(self):
#         '''
#         Returns the first_name plus the last_name, with a space in between.
#         '''
#         full_name = self.username
#         return full_name.strip()
#
#     def get_short_name(self):
#         '''
#         Returns the short name for the user.
#         '''
#         return self.username
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         '''
#         Sends an email to this User.
#         '''
#         # send_mail(subject, message, from_email, [self.email], **kwargs)
#         pass
from Skill.models import Skill


class User(AbstractUser):
    austr = 'AUS'
    rus = 'RUS'
    usa = 'USA'
    mex = 'MEX'
    CHOISES_LOCATION = ((austr, 'Australia'), (rus, 'Russia'), (usa, 'USA'), (mex, 'Mexico'))
    location = models.CharField(max_length=3, choices=CHOISES_LOCATION, default=usa)
    # username = models.CharField(max_length=30, unique=True)
    # password = models.TextField()
    skills = models.TextField(max_length=600)
    was_processed = models.BooleanField(default=False)
    skills_processed = models.TextField(max_length=600)
    skills_key = models.ManyToManyField(Skill)