from django.views.generic.base import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', TemplateView.as_view(template_name='upload.html'), name='upload'),
    path('loader/', TemplateView.as_view(template_name='loader.html'), name='loader'),
    path('results/', TemplateView.as_view(template_name='results.html'), name='results'),
]