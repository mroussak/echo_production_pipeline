from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from time import time, sleep
from EchoAnalyzer.models import File, Visit
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
    
    visit, created = Visit.objects.get_or_create(user=request.user, processed_at=None)
   
    File.objects.create(
        file=request.FILES.get('filePond'),
        user=request.user,
        visit=visit
    )

    return HttpResponse(json.dumps({'success': True}))
    
    
    
@login_required(login_url='/login/')    
def execute_pipeline(request):
    
    if request.method=='POST':
    
        user_id = request.POST.get('user_id', '')
        session_id = '1'
        visit =  Visit.objects.get(user_id=request.user, processed_at=None)
        # send the visit.id to the Production Pipeline
        
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