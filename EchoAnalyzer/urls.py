from django.views.generic.base import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.LoadUploadPage, name='upload'),
    path('handle-upload/<int:visit_id>/', views.HandleUpload, name='handle-upload'),
    path('loader/<int:visit_id>/', views.LoadLoaderPage, name='loader'),
    #path('loader/', views.LoadLoaderPage, name='loader'),
    path('execute_pipeline/',  views.ExecutePipeline, name='execute_pipeline'),
    path('check_visit_status/', views.CheckVisitStatus, name='check_visit_status'),
    path('results/<int:visit_id>/', views.LoadResultsPage, name='results'),
    #npath('results/', TemplateView.as_view(template_name='results.html'), name='results'),
]
