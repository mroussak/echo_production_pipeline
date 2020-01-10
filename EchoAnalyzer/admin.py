from EchoAnalyzer.models import File, Visit
from django.contrib import admin



class FileInline(admin.TabularInline):
    model = File
    
    

class FileAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'get_file', 'file_name', 'user', 'processing_time',  'created_at', 'visit', 'log_preview', 'dicom_id', 'started_processing_at', 'finished_processing_at')
    list_display_links = ['id', 'log_preview']
    
    search_fields = ('id', 'user__email', 'file', 'file_name',)
    
    
    def get_file(self, instance):
        return instance.file
    get_file.short_description = 'File (S3 Key)'
    
    
class VisitAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'user_email', 'processing_time', 'results_preview', 'file_list',  'created_at', 'started_processing_at', 'finished_processing_at',)
    list_display_links = ['id', 'results_preview']

    def file_list(self, instance):
        return list(instance.file_set.all().values_list('file_name', flat=True))



admin.site.register(File, FileAdmin)
admin.site.register(Visit, VisitAdmin)

