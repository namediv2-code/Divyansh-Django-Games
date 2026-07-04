from django.urls import path
from . import views

urlpatterns = [
    path('', views.navigation, name='navigation'),
    path('userguess/', views.guessno, name='guessno'),
    path('rps/',views.home, name='home'),
    path('cricket/',views.cricket, name='cricket'),
    path('cricketrules/',views.crules,name='crules'),
    path('trivia/',views.trivia,name='trivia'),
    path('computerguesses/',views.computerGuesses,name='computerGuesses'),
    path('guess/',views.gnav,name='gnav'),
    path('click/',views.clicker,name='clicker'),
    path('cach/',views.cach,name='cach'),
    path('equipment/',views.equipment,name='equipment'),
    path('get_clicks/', views.get_clicks, name='get_clicks'),
]