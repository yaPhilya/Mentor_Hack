from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
import django.contrib.auth.forms as forms
# from User.form import UserForm


# def signup(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('main.html')
#     else:
#         form = UserForm()
#     return render(request, 'signup.html', {'form': form})


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
                # username = data['username']
                # if (data['password1'] == data['password2']):
                #     raw_password = data['password1']
                # else:
                #     return HttpResponse("Passwords don't match")
                #
                # user = authenticate(username=username, password=raw_password)
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