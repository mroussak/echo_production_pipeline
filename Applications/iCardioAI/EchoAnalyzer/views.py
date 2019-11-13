from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from time import time, sleep
import json
import sys

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline')
from Components.Models import ModelsPipeline
import Tools.ProductionTools as tools
import ProductionPipeline



# Create your views here.
@login_required(login_url='/login/')
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
    
    
    
@login_required(login_url='/login/')    
def execute_pipeline(request):
    
    if request.method=='POST':
    
        user_id = request.POST.get('user_id', '')
        session_id = '1'
        
        #ProductionPipeline.main(user_id, session_id, verbose=True, start=time())
    
    return render(request, template_name='loader.html')
    
    


@login_required(login_url='/login/')
def send_report(request):
    
    user_id = request.POST.get('user_id', '')
    session_id = '1'
        
    reports_file_path = '/internal_drive/Users/daniel@icardio.ai/Sessions/1/Reports/reports.json'
    
    with open(reports_file_path) as json_file:
        report = json.load(json_file)
        
    json_object = json.dumps(report)
    
    return render(request, "results.html", {'report_json': json_object})