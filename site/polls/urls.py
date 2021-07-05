from django.urls import path
from . import views

import sys
sys.path.append('../site/static/script')
from scomblogin import *
from kadaiadd import *

urlpatterns = [
    path('', views.index_templates, name="index_templates"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('home/',views.HomeView.as_view(), name="home"),
    path('kadai/',views.KadaiView.as_view(), name="kadai"),
    path('kadaiadd/',views.KadaiaddView.as_view(), name="kadaiadd"),
    path('login/create/', views.UserCreateView.as_view(),name="create"),
    path('createok/', views.UserCreateokView.as_view(),name="createok"),
    path('home/scomblogin',ScombLoginView.as_view(),name="scomblogin"),
    path('home/scomblogin/ajax',ajax,name="scomblogin_ajax"),
    path('kadaiadd/ajax',kadaiaddajax,name="kadaiadd_ajax"),
]
