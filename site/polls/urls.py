from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_templates, name="index_templates"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('home/',views.HomeView.as_view(), name="home"),
    path('login/create/', views.UserCreateView.as_view(),name="create"),
    path('createok/', views.UserCreateokView.as_view(),name="createok"),
    path('home/scomblogin',views. ScombLoginView.as_view(),name="scomblogin"),
]
