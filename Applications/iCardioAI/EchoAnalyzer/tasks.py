from __future__ import absolute_import, unicode_literals
import os
import sys
from celery import shared_task
from decouple import config

from time import time
sys.path.insert(1, config('BASE_DIR') + 'echo_production_pipeline/Pipeline/ProductionPipeline')

from Components.Models import ModelsPipeline
import Tools.ProductionTools as tools
import ProductionPipeline


try:
    # next line will raise exception in django, but will work fine in celery
    is_worker = os.environ['celery_worker']  
    ret = ModelsPipeline.main(verbose=True, start=time())
    print(ret)
except Exception as exc:
    # django code will catch exception that celery_worker doesn't exist and print it here
    print(exc)



@shared_task
def start_pipeline(username, visit_id, file_list=[], verbose=True, start=None):
    if not start:
        start = time()
    root_directory = tools.BuildRootDirectory(username, str(visit_id))
    tools.BuildDirectoryTree(root_directory)
    ProductionPipeline.main(username, str(visit_id), s3_files=file_list, verbose=verbose, start=start, views_model=ret[0], graph=ret[1])