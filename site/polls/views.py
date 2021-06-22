from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView # 追記
from django.contrib.auth.forms import UserCreationForm  # 追記
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse

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
    form_class = forms.LoginForm
    template_name = "scomblogin.html"

class KadaiView(TemplateView):
    template_name = "kadai.html"

class KadaiAddView(TemplateView):
    template_name = "kadaiadd.html"
class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context