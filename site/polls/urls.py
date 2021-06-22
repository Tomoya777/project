from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_templates, name="index_templates"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('home/',views.HomeView.as_view(), name="home"),
    path('kadai/',views.KadaiView.as_view(), name="kadai"),
    path('kadaiadd/',views.KadaiAddView.as_view(), name="kadaiadd"),
    path('login/create/', views.UserCreateView.as_view(),name="create"),
    path('createok/', views.UserCreateokView.as_view(),name="createok"),
    path('home/scomblogin',views. ScombLoginView.as_view(),name="scomblogin"),
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path(
        'mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'
    ),
]
