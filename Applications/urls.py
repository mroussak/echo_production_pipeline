from django.views.generic.base import TemplateView
from django.urls import path
from . import views


urlpatterns = [
    path('apps/', views.AppsList, name='apps'), # app web page
    path('', views.AppsList, name='apps'), # default web page
]