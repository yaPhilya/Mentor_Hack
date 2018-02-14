from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
import django.contrib.auth.forms as forms
from Resume.models import Resume
from User.models import User


def userpage(request, u_id):
    user = User.objects.get(id=u_id)
    # if request.method == 'POST':
    #     form = ResumeCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form.instance.user = user
    #         return redirect('users:userpage', {'u': user})
    # else:
    #     form = ResumeCreationForm()
    resumes = Resume.objects.filter(user_id=user.id)
    return render(request, 'user_page.html', {'u': user, 'resumes': resumes})


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = "username", "password1", "password2", "location", "skills"

    def label_tag(self, contents=None, attrs=None):
        pass

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        pass

    def signup(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('main')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


class AuthenticationForm(forms.AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = "username", "password1", "password2"

    def label_tag(self, contents=None, attrs=None):
        pass

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        pass

    def login(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('main')
        else:
            form = UserCreationForm()
            return render(request, 'login.html', {'form': form})