from django.contrib.auth.decorators import login_required
from EchoAnalyzer.models import File, Visit, hash_file
from django.contrib.messages import get_messages
from EchoAnalyzer.tasks import ProcessVisit
from WebTools.Tools import PrintTitle
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from time import time, sleep
import traceback
import json
import sys



sys.path.insert(1, '/echo_pipeline/Pipeline/')
from ProductionPipeline import ProductionPipeline



@login_required(login_url='/login/')
def LoadUploadPage(request):
    
    ''' Accepts request from /upload, creates visit object, renders upload page ''' 
    
    PrintTitle('EchoAnalyzer.views.LoadUploadPage')
    
    # create visit object:
    visit = Visit.objects.create(user=request.user, user_email=request.user.email)

    # debug:
    print('[EchoAnalyzer.views.Upload] Got request from user with user id [%s]' %request.user)
    print('[EchoAnalyzer.views.Upload] Got request from user with visit id [%s]' %visit.pk)

    return render(request, 'upload.html', {'visit_id': visit.pk})



@login_required(login_url='/login/')
def HandleUpload(request, visit_id):
    
    ''' Accepts request, visit_id, downloads files and saves them to visit object '''
    
    PrintTitle('EchoAnalyzer.views.HandleUpload')
    
    try:
        
        # debug:
        print('[EchoAnalyzer.views.HandleUpload]: Got request.FILES.get("filePond") [%s]' %request.FILES.get('filePond'))
        
        # unpack request:
        file_kwargs = {
            'file' : request.FILES.get('filePond'),
            'file_name' : request.FILES.get('filePond'),
            'dicom_id' : None, # update this field later
            'user' : request.user,
            'user_email' : request.user.email,
            'visit' : Visit.objects.get(pk=visit_id, user=request.user),
        }
        
        # create file objects and associate to visit:
        file = File.objects.create(**file_kwargs)
        
        # update dicom_id field:
        file.dicom_id = str(file.file)
        file.save()
        
        success = True
        status = 0
        internal_message = 'successfully uploaded file [%s]' %file_kwargs['file_name']
        message = 'Uploaded file successfully.'

    except Exception as error:
        
        success = False
        status = 1
        internal_message = error
        message = 'Error when uploading file.'
        
    result = {
        'success': success,
        'status' : status,
        'message' : message,
    }

    print('[EchoAnalyzer.views.HandleUpload]: Status [%d], Internal Message [%s], Message [%s]' %(status, internal_message, message))

    return HttpResponse(json.dumps(result))
    
    
    
@login_required(login_url='/login/')    
def LoadLoaderPage(request, visit_id):
    
    ''' Accepts request to /loader, renders loader page '''
    
    PrintTitle('EchoAnalyzer.views.LoadLoaderPage')
    
    try:
        
        # debug:
        print('[EchoAnalyzer.views.LoadLoaderPage]: Got post request with [%s]' %request.POST)
        
        # unpack post request:
        user_id = request.user
        #visit_id = request.POST['visit_id']
        
        success = True
        status = 0
        internal_message = 'routed to loader with user id [%s] and visit id [%s]' %(user_id, visit_id)
        message = 'We are processing your data.'

    except Exception as error:
        
        visit_id = -1
        
        success = False
        status = 1
        internal_message = error
        message = 'Error when rendering loader page.'
        
    result = {
        'success': success,
        'status' : status,
        'message' : message,
        'visit_id' : visit_id,
    }

    print('[EchoAnalyzer.views.LoadLoaderPage]: Status [%d], Internal Message [%s], Message [%s]' %(status, internal_message, message))        
    
    return render(request, 'loader.html', context=result)



@login_required(login_url='/login/')    
def ExecutePipeline(request):
    
    ''' Accepts request tp /execute_pipeline, executes production pipeline '''
    
    PrintTitle('EchoAnalyzer.views.ExecutePipeline')
    
    try:
        
        # unpack post request:
        user_id = request.user.email
        visit_id = request.POST['visit_id']
        
        # get visit object by id:
        visit = Visit.objects.get(pk=visit_id, user_id=request.user)
        
        # debug:
        print('[EchoAnalyzer.views.ExecutePipeline]: Got post request with [%s]' %request.POST)
        
        # execute pipeline if not already started:
        if not visit.started_processing_at:
            result = ProcessVisit(user_id, visit_id)
            
        success = True
        status = 0
        internal_message = 'pipeline success for visit with id [%s]' %visit_id
        message = 'Data processed!'

    except Exception as error:
        
        success = False
        status = 1
        internal_message = traceback.format_exc()
        message = 'Error, could not process your data.'
        
    result = {
        'success': success,
        'status' : status,
        'message' : message,
        'visit_id' : visit_id,
    }

    print('[EchoAnalyzer.views.ExecutePipeline]: Status [%d], Internal Message [%s], Message [%s]' %(status, internal_message, message))      

    return HttpResponse(json.dumps(result), content_type='application/json')
    


@login_required(login_url='/login/')    
def CheckVisitStatus(request):
    
    ''' Accepts request to check_visit_status, checks if pipeline completed '''
    
    PrintTitle('EchoAnalyzer.views.CheckVisitStatus')
    
    try:
        
        # debug:
        print('[EchoAnalyzer.views.CheckVisitStatus]: Got post request with [%s]' %request.POST)
        
        # unpack post request:
        user = request.user
        visit_id = request.POST['visit_id']
        
        # get visit object by id:
        visit = Visit.objects.get(pk=visit_id, user_id=request.user)
        
        if visit.results and visit.finished_processing_at:
        
            success = True
            status = 0
            internal_message = 'pipeline complete for visit with id [%s]' %visit_id
            message = 'Data processed!'

        else:
        
            success = False
            status = 0
            internal_message = 'pipeline processing for visit with id [%s]' %visit_id
            message = 'We are processing your data.'

    except Exception as error:
        
        success = False
        status = 1
        internal_message = error
        message = 'Error, could not process your data.'
        
    result = {
        'success': success,
        'status' : status,
        'message' : message,
        'visit_id' : visit_id,
    }

    print('[EchoAnalyzer.views.CheckVisitStatus]: Status [%d], Internal Message [%s], Message [%s]' %(status, internal_message, message))      

    return HttpResponse(json.dumps(result), content_type='application/json')
    
    

@login_required(login_url='/login/')    
def LoadResultsPage(request, visit_id):
    
    ''' Accepts request to results/, checks if pipeline completed '''
    
    PrintTitle('EchoAnalyzer.views.CheckVisitStatus')
    
    try:
        
        # debug:
        print('[EchoAnalyzer.views.LoadResultsPage]: Got post request with [%s]' %request.POST)
        
        # unpack post request:
        user = request.user

        # get visit object by id:
        visit = Visit.objects.get(pk=visit_id, user_id=request.user)
        
        results = visit.results
        
        success = True
        status = 0
        internal_message = 'sent results for visit with id [%s]' %visit_id
        message = 'Results sent.'
        

    except Exception as error:
        
        results = 0
        
        success = False
        status = 1
        internal_message = error
        message = 'Error, could not find your results.'
        
    result = {
        'success': success,
        'status' : status,
        'message' : message,
        'visit_id' : visit_id,
        'results' : results,
    }

    print('[EchoAnalyzer.views.CheckVisitStatus]: Status [%d], Internal Message [%s], Message [%s]' %(status, internal_message, message))      

    return render(request, 'temp_results.html', context = result)
    #return HttpResponse(json.dumps(result), content_type='application/json')
    