from django.contrib import admin
from Resume.models import Resume
from Skill.models import Skill
from User.models import User

admin.site.register(Resume)
admin.site.register(User)
admin.site.register(Skill)