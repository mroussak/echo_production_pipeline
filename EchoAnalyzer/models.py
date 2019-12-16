from django.contrib.postgres.fields import JSONField
from functools import partial
from django.db import models
import hashlib
import os



def hash_file(file, block_size=65536):
    
    hasher = hashlib.md5()
    
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()



def upload_to(instance, filename):
    
    ''' :type instance: dolphin.models.File '''
    
    instance.file.open()
    
    return hash_file(instance.file)
    
    
    
class Visit(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    user_email = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_processing_at = models.DateTimeField(null=True, blank=True)
    finished_processing_at = models.DateTimeField(null=True, blank=True)
    results = JSONField(null=True, blank=True)

    @property
    def results_preview(self):
        
        if self.results:
            return 'Click to see results.'
        else:
            return 'No results.'
        
        

class File(models.Model):
    file = models.FileField(upload_to=upload_to)
    file_name = models.TextField(null=True, blank=True)
    dicom_id = models.TextField(null=True, blank=True)
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    user_email = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)
    log = models.TextField(null=True, blank=True)
    started_processing_at = models.DateTimeField(null=True, blank=True)
    finished_processing_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def log_preview(self):
        return 'Click to see log.'