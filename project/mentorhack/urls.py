from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView

from Main.views import main, results
from Resume.views import NewResume
from User.views import UserCreationForm, AuthenticationForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main, name='main'),
    url(r'^signup/$', UserCreationForm.signup, name='signup'),
    # url(r'^login/$', AuthenticationForm.login, name='login'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name="login"),
    url(r'^logout/$', LogoutView.as_view(template_name='logout.html'), name='logout'),
    url(r'^users/', include('User.urls', namespace='users')),
    url(r'^createresume', NewResume.as_view(), name='createresume'),
    url(r'^results/(?P<resume_id>\d+)/$', results, name='results')
]
# urlpatterns += [
#     url(r'^static/(?P<path>.*)$','django.views.static.serve')
# ]
