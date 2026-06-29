from django.urls import path
from . import views

urlpatterns = [
    path('', views.navigation, name='navigation'),
    path('guess/', views.guessno, name='guessno'),
    path('rps/',views.home, name='home'),
    path('cricket/',views.cricket, name='cricket'),
    path('cricketrules/',views.crules,name='crules'),
]