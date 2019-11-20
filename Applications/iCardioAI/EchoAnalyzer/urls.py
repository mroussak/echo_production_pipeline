from django.views.generic.base import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('loader/<int:pk>/',  views.execute_pipeline, name='loader'),
    #path('results/', TemplateView.as_view(template_name='results.html'), name='results'),
    path('handle-upload/<int:pk>/', views.handle_upload, name='handle-upload'),
    path('results/<int:pk>', views.send_report, name='results'),
    path('status/<int:pk>', views.visit_status, name='visit_status'),
]
