from django.urls import path
from . import views


urlpatterns = [
    #path('register/', views.Register.as_view(), name='register'),
    path('register/', views.Register, name='register'),
]