from django.contrib import admin
from django.urls import path
from myapp.views import hello
from . import views

urlpatterns = [
    #path('', views.users)
    path('', views.BASE, name='BASE'),
]