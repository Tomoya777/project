from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse

from django.core.mail import send_mail

def index_templates(request):
    return render(request, 'index.html')

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "logout.html"

class HomeView(TemplateView):
    template_name = "home.html"

class kadaiView(TemplateView):
    template_name = "kadai.html"

class kadaiaddView(TemplateView):
    template_name = "kadaiadd.html"

class UserCreateView(CreateView):
    form_class = forms.UserCreationForm
    template_name = "create.html"
    success_url = reverse_lazy("createok")

class UserCreateokView(TemplateView):

    template_name = "createok.html"

class ScombLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "scomblogin.html"
