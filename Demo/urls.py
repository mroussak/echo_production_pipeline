from django.views.generic.base import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('demo/', views.Demo, name='demo'),
    path('demo/sonoscanner/', views.DemoSonoscanner, name='demo_sonoscanner'),
    path('demo/ge_vingmed_ultrasound/', views.DemoGEVingmedUltrasound, name='demo_ge_vingmed_ultrasound'),
]
