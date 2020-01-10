import traceback
import json
import sys

from time import time, sleep

from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

from EchoAnalyzer.models import File, Visit, hash_file
from EchoAnalyzer.utils import get_s3
from WebTools.Tools import PrintTitle
from EchoAnalyzer.features import FEATURES



global DEMO_VISIT_ID
DEMO_VISIT_ID = 817



def AddMediaLinks(results):
    
    ''' Accepts results object, appends media links to results object '''
    
    # connect to s3:
    s3 = get_s3()
    
    # add s3 links to media files:
    for result in results['results']:

        # initialize empty links dictionary:
        result['links'] = {}

        # get s3 link for each item in media:
        for key, value in result['media'].items():

            # create s3 url params:
            Params = {
                'Bucket' : settings.AWS_S3_BUCKET_NAME,
                'Key' : result['media'][key][1:] # drop initial '/' in s3_key name
            }
            
            # get url:
            url = s3.generate_presigned_url(ClientMethod='get_object', Params=Params, ExpiresIn=3600)
            
            # append url to result object:
            result['links'][key] = url
        
        # get list of features:
        if result['view'] is not None:
            view = result['view']['predicted_view']
            result['view']['features'] = FEATURES[view]
            
            # multiply confidences by 100 (to be percentages):
            result['view']['abnormality_confidence'] *= 100
            result['view']['view_confidence'] *= 100

    return results

    
    
def Demo(request):
    
    ''' Accepts request to demo/, loads demo page '''
    
    PrintTitle('Demo.views.Demo')
    
    try:
        
        # debug:
        print('[Demo.views.Demo]: Got post request with [%s]' %request.POST)
        
        # set demo visit id:
        demo_visit_id = DEMO_VISIT_ID
        
        # get visit object by id:
        visit = Visit.objects.get(pk=demo_visit_id)
        results = visit.results
        
        # add s3 links to media files:
        results = AddMediaLinks(results)
        
        success = True
        status = 0
        internal_message = 'sent results for visit with id [%s]' %demo_visit_id
        message = 'Results sent.'
        
    except Exception as error:
        
        results = -1
        
        success = False
        status = 1
        internal_message = traceback.format_exc()
        message = 'Error, could not find your results.'
        
    result = {
        'success': success,
        'status' : status,
        'message' : message,
        'visit_id' : demo_visit_id,
        'results' : results,
    }

    print('[EchoAnalyzer.views.LoadResultsPage]: Status [%d], Internal Message [%s], Message [%s]' %(status, internal_message, message))      

    return render(request, 'temp_results.html', context = result)