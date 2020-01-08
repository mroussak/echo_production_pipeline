from django.views.generic.base import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('demo/', views.Demo, name='demo'),
]
