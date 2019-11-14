import os
import hashlib
from functools import partial
from django.db import models

# Create your models here.

def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()


def upload_to(instance, filename):
    """
    :type instance: dolphin.models.File
    """
    instance.file.open()
    filename_base, filename_ext = os.path.splitext(filename)

    return "{0}.{1}".format(hash_file(instance.file), filename_ext)
    
    
class Visit(models.Model):
     user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
     processed_at = models.DateTimeField(null=True)
     created_at = models.DateTimeField(auto_now_add=True)
    

class File(models.Model):
    file = models.FileField(upload_to=upload_to)
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True)
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)

    
    # SELECT * FROM echoanalyzer_file WHERE user_id = 1 and processed_at is null