from django.http import HttpResponse
from django.shortcuts import render
from time import time
import json
import sys

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline')
from Components.Models import ModelsPipeline
import Tools.ProductionTools as tools
import ProductionPipeline


# Create your views here.
def upload(request):
    session_id = '1'
    root_directory = tools.BuildRootDirectory(request.user.username, session_id)
    tools.BuildDirectoryTree(root_directory)
    print(request.FILES)
    for count, x in enumerate(request.FILES.getlist("filePond")):
        def process(f):
            path = '/internal_drive/Users/{username}/Sessions/{session_id}/Dicoms/{count}'.format(
                username=request.user.username,
                session_id=session_id,
                count=f.name
            )
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk) 
        process(x)
    return HttpResponse(json.dumps({'success': True}))
    
    
    
def execute_pipeline(request):
    
    user_id = request.user.username
    session_id = '1'
    
    ProductionPipeline.main(user_id, session_id, verbose=True, start=time())