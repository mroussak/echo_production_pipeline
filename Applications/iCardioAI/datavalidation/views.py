from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, time, timedelta
import sys
import os

# Database imports:
#sys.path.insert(1, '/internal_drive/echo_production_pipeline/Database/EchoData/')
sys.path.insert(1, '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/')
import PostgresCaller



@login_required(login_url='/login/')
def DataValidation(request):

    # intialize variables:
    result = None
    
    if 'previous_object_id' not in request.session:
        request.session['previous_object_id'] = -1

    # list of queries:
    web_app_queries = {
        'SELECT_get_next_unlabeled_view' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/SELECT_get_next_unlabeled_view.psql',
        'UPDATE_add_previous_object_id' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_add_previous_object_id.psql',
        'UPDATE_add_view_label_to_row' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_add_view_label_to_row.psql',
        'UPDATE_set_view_to_in_use' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_set_view_to_in_use.psql',
        'UPDATE_set_view_to_not_in_use' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_set_view_to_not_in_use.psql',
    }

    #query_file = web_app_queries['SELECT_get_next_unlabeled_view']
    #query_file = web_app_queries['UPDATE_add_previous_object_id']
    #query_file = web_app_queries['UPDATE_add_view_label_to_row']
    #query_file = web_app_queries['UPDATE_set_view_to_in_use']
    #query_file = web_app_queries['UPDATE_set_view_to_not_in_use']
    
   
    if request.method == 'POST':
        
        # get labels:
        parameters = {
            'object_id' : request.POST.get("object_id", ""),
            'view' : request.POST.get("view", ""),
            'subview' : request.POST.get("subview", ""),
            'quality' : request.POST.get("quality", ""),
            # 'quality1' : request.POST.get("quality1", ""), 
            # 'quality2' : request.POST.get("quality2", ""),
            # 'quality3' : request.POST.get("quality3", ""),
            # 'quality4' : request.POST.get("quality4", ""),
            # 'quality5' : request.POST.get("quality5", ""),
            'user_id' : request.POST.get("user_id", ""),
            'selection_time' : datetime.strptime(request.POST.get("selection_time", ""),'%f'),
            'time_stamp' : datetime.now(),
            'previous_object_id' : request.session['previous_object_id'],
        }
        
        # set view to not in use:
        query_file = web_app_queries['UPDATE_set_view_to_not_in_use']
        PostgresCaller.main(query_file, parameters, verbose=True, start=time())
        
        # update table:
        query_file = web_app_queries['UPDATE_add_view_label_to_row']
        PostgresCaller.main(query_file, parameters, verbose=True, start=time())
        
        # update previous object id field:
        request.session['previous_object_id'] = parameters['object_id']
        
        # debug
        print('previous object id in POST: %s' %request.session['previous_object_id'])
        print('[POST REQUEST]__')
        print('[UPDATE QUERY]__')
        print(parameters)
        
        # get next view:
        query_file = web_app_queries['SELECT_get_next_unlabeled_view']
        result = PostgresCaller.main(query_file, parameters, verbose=True, start=time())
        result = result.to_dict(orient='records')[0]
        result = {'result' : result}
        
        # set view to in use:
        parameters = {
            'object_id' : result['result']['object_id'],
        }
        query_file = web_app_queries['UPDATE_set_view_to_in_use']
        PostgresCaller.main(query_file, parameters, verbose=True, start=time())
        
        # debug:
        print('[SELECT QUERY]__')
        print(result)
     
     
    if request.method == 'GET':
        
        if request.GET.get("previous_object_id", ""):
            
            query_file = web_app_queries['SELECT_get_next_unlabeled_view']
            result = PostgresCaller.main(query_file, parameters, verbose=True, start=time())
            result = result.to_dict(orient='records')[0]
            result = {'result' : result}
    
            print('previous object id in GET PREVIOUS: %s' %request.session['previous_object_id'])
            
            print('[GET REQUEST]__')
            print('[SELECT QUERY]__')
            print('getting previous object...')
        
        else:
            query_file = web_app_queries['SELECT_get_next_unlabeled_view']
            parameters = None
            result = PostgresCaller.main(query_file, parameters, verbose=True, start=time())
            result = result.to_dict(orient='records')[0]
            result = {'result' : result}
           
            print('previous object id in GET: %s' %request.session['previous_object_id'])
            
            print('[GET REQUEST]__')
            print('[SELECT QUERY]__')
            print(result)
        
    
    return render(request, template_name='validator.html', context=result)