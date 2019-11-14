from EchoAnalyzer.models import File, Visit
from django.contrib import admin

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'created_at', 'processed_at', 'visit',)
    


admin.site.register(File)
admin.site.register(Visit)

