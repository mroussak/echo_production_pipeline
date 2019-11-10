from django.views.generic.base import TemplateView
from django.urls import path
from . import views


urlpatterns = [
    path('validator/', views.DataValidation, name='validator'),
]