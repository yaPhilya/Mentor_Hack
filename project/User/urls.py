from django.conf.urls import url

from User.views import userpage

urlpatterns = [
    url(r'^(?P<u_id>\d+)/$', userpage, name='userpage')
]