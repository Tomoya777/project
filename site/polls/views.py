from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from taskdatabase import *

def index_templates(request):
    return render(request, 'index.html')

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "logout.html"

class HomeView(TemplateView):
    template_name = "home.html"

class UserCreateView(CreateView):
    form_class = forms.UserCreationForm
    template_name = "create.html"
    success_url = reverse_lazy("createok")

class UserCreateokView(TemplateView):
    template_name = "createok.html"

class ScombLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        context = {
            'message': "POST method OK!!",
        }
        return render(request, 'scomblogin.html', context)

    def get(self, request, *args, **kwargs):
        context = {
            'message': "Hello World! from View!!",
        }
        return render(request, 'scomblogin.html', context)

class KadaiView(TemplateView):
    def get(self, request, *args, **kwargs):
        code ,task_list = taskdata_ask(str(self.request.user))
        task_list_export = []
        for task_temp in task_list:
            if (bool(task_temp["can_submit"])) == True:
                task_list_export.append(task_temp)
        context = {
            'task_list': task_list_export,
        }
        return render(request, 'kadai.html', context)
    def post (self, request, *args, **kwargs):
        print(request.POST.get("task_value"))
        context = {
            'subject_name' : request.POST.get("subject_name"),
            'estimated_time' : request.POST.get("estimated_time"),
            'progress' : request.POST.get("progress"),
            'submit_time_date' : request.POST.get("submit_time")[:10],
            'submit_time_time' : request.POST.get("submit_time")[11:16],
            'remarks' : request.POST.get("remarks"),
            'task_id' : request.POST.get("task_id"),
            'can_submit' : request.POST.get("can_submit"),
            'submit_url' : request.POST.get("submit_url"),
            'task_name' : request.POST.get("task_name"),
        }
        return render(request, 'kadaiadd.html', context)


class KadaiaddView(TemplateView):
    template_name = "kadaiadd.html"
