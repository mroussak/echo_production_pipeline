from django.contrib.auth.decorators import login_required
from EchoAnalyzer.models import File, Visit
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from time import time, sleep
from EchoAnalyzer.tasks import start_pipeline
import json


@login_required(login_url='/login/')
def upload(request):
    
    ''' Accepts request from /upload, creates visit object ''' 
    
    visit = Visit.objects.create(user=request.user, user_email=request.user.email)
    
    return render(request, 'upload.html', {'visit_id': visit.pk})



@login_required(login_url='/login/')
def handle_upload(request, pk):
    
    ''' Accepts request, visit.id as pk,, downloads files and saves them to visit object '''
    
    # debug:
    print('[EchoAnalyzer.views.handle_upload]: retreived files [%s]' %request.FILES)
    
    # get visit object with given id:
    visit = Visit.objects.get(pk=pk, user=request.user)
   
    # create file objects and associate to visist:
    File.objects.create(
        file=request.FILES.get('filePond'),
        user=request.user,
        user_email = request.user.email,
        visit=visit
    )

    return HttpResponse(json.dumps({'success': True}))
    
    
    
@login_required(login_url='/login/')    
def execute_pipeline(request, pk):
    
    ''' Accepts visit_id as pk, executes production pipeline '''
    
    # get visit object by id:
    visit =  Visit.objects.get(pk=pk, user_id=request.user)
    
    # execute pipeline if not already started:
    if not visit.started_processing_at:
        file_list = list(visit.file_set.all().values_list('file', flat=True))
        #import pdb; pdb.set_trace()
        print(file_list)
        start_pipeline.delay(request.user.username, str(visit.id), file_list, verbose=True)
    
    return render(request, 'loader.html', {'visit_id': visit.id})
    


@login_required(login_url='/login/')    
def visit_status(request, pk):
    
    ''' Accepts request, visit.id as pk, returns status of pipeline '''
    
    # get visit object by id:
    visit =  Visit.objects.get(pk=pk, user_id=request.user)
    
    # reroute user if pipeline is complete:
    if visit.results and visit.processed_at:
        return HttpResponse(json.dumps({'status':'done', 'url': reverse('results', kwargs={'pk': visit.pk})}), status=201, content_type='application/json')
        
    return HttpResponse(json.dumps({'status': 'not-done', 'log': visit.log}), content_type='application/json')
    


@login_required(login_url='/login/')
def send_report(request, pk):
    
    ''' Accepts request, visit.id as pk, returns result from pipeline as json object '''
    
    # get result object by id:
    visit =  Visit.objects.get(pk=pk, user_id=request.user)
    
    return render(request, "results.html", {'report_json': json.dumps(visit.results), 'visit': visit})