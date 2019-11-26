from django.contrib.auth.decorators import login_required
import ViewsLabeler.ViewsLabelerFunctions as funcs
from datetime import datetime, time, timedelta
from django.shortcuts import render
from decouple import config
import sys
import os

# Database imports:
sys.path.insert(1, config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/')
import PostgresCaller



@login_required(login_url='/login/')
def DataValidation(request):

    # intialize variables:
    result = None
    kwargs = {
        'verbose' : False,
        'start' : time(),
    }
    
    if 'previous_object_id' not in request.session:
        request.session['previous_object_id'] = '-1'

    # list of queries:
    web_app_queries = {
        'SELECT_get_next_unlabeled_view' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/SELECT_get_next_unlabeled_view.sql',
        'SELECT_get_previous_view' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/SELECT_get_previous_view.sql',
        'SELECT_get_total_labels' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/SELECT_get_total_labels.sql',
        'UPDATE_add_previous_object_id' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/UPDATE_add_previous_object_id.sql',
        'UPDATE_add_view_label_to_row' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/UPDATE_add_view_label_to_row.sql',
        'UPDATE_set_view_to_in_use' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/UPDATE_set_view_to_in_use.sql',
        'UPDATE_set_view_to_not_in_use' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/WebAppQueries/UPDATE_set_view_to_not_in_use.sql',
    }

    
    
   
    if request.method == 'POST':
        
        if 'previous_object_id' in request.POST:
            
            # get parameters from post request:
            parameters = {
                'object_id' : request.POST.get('object_id', ''),
                'previous_object_id' : request.POST.get('previous_object_id', ''),
            }
            
            # set view to not in use:
            query_file = web_app_queries['UPDATE_set_view_to_not_in_use']
            PostgresCaller.main(query_file, parameters, **kwargs)
 
            # select previous view:
            query_file = web_app_queries['SELECT_get_previous_view']
            result = PostgresCaller.main(query_file, parameters, **kwargs)
            result = result.to_dict(orient='records')[0]
            result = {'result' : result}
            
            # get total label count:
            count_query = web_app_queries['SELECT_get_total_labels']
            count_parameters = {
                'user_id' : request.user.email,
            }
            count_result = PostgresCaller.main(count_query, count_parameters, **kwargs)
            count = int(count_result.iloc[0]) 
            result['result']['count'] = count
            
            print()
            print('[POST]--[PREVIOUS]--[START]')
            print('[POST]--[PREVIOUS]--[PARAMETERS] (parameters from front end)')
            print(parameters)
            print()
            
            # set view to in use:
            parameters = {
                'object_id' : result['result']['object_id'],
                'previous_object_id' : result['result']['previous_object_id'],
            }
            query_file = web_app_queries['UPDATE_set_view_to_in_use']
            PostgresCaller.main(query_file, parameters, **kwargs)
            
            print('[POST]--[PREVIOUS]--[PARAMETERS] (parameters to set view to "in use")')
            print(parameters)
            print()
            print('[POST]--[PREVIOUS]--[RESULT] (data pulled from database with these values)')
            print(result)
            print()
            print('[POST]--[PREVIOUS]--[END]')

        else:
            
            # get labels:
            parameters = funcs.ParseLabels(request, **kwargs)
            
            # set view to not in use:
            query_file = web_app_queries['UPDATE_set_view_to_not_in_use']
            PostgresCaller.main(query_file, parameters, **kwargs)
            
            # update table:
            query_file = web_app_queries['UPDATE_add_view_label_to_row']
            PostgresCaller.main(query_file, parameters, **kwargs)
            
            # update previous object id field:
            request.session['previous_object_id'] = parameters['object_id']
            
            # get next view:
            query_file = web_app_queries['SELECT_get_next_unlabeled_view']
            result = PostgresCaller.main(query_file, parameters, **kwargs)
            result = result.to_dict(orient='records')[0]
            result = {'result' : result}
            result['result']['previous_object_id'] = request.session['previous_object_id']
            
            # get total label count:
            count_query = web_app_queries['SELECT_get_total_labels']
            count_parameters = {
                'user_id' : request.user.email,
            }
            count_result = PostgresCaller.main(count_query, count_parameters, **kwargs)
            count = int(count_result.iloc[0]) 
            result['result']['count'] = count
            
            print()
            print('[POST]--[NEXT]--[START]')
            print('[POST]--[NEXT]--[PARAMETERS] (database updated with these values)')
            print(parameters)
            print()
            
            # set view to in use:
            parameters = {
                'object_id' : result['result']['object_id'],
                'previous_object_id' : request.session['previous_object_id'],
            }
            query_file = web_app_queries['UPDATE_set_view_to_in_use']
            PostgresCaller.main(query_file, parameters, **kwargs)
            
            print('[POST]--[NEXT]--[PARAMETERS] (to set view to "in use")')
            print(parameters)
            print()
            print('[POST]--[NEXT]--[RESULT] (data pulled from database with these values)')
            print(result)
            print()
            print('[POST]--[NEXT]--[END]')
     
     
    if request.method == 'GET':
        
        # get new view:
        query_file = web_app_queries['SELECT_get_next_unlabeled_view']
        parameters = None
        result = PostgresCaller.main(query_file, parameters, **kwargs)
        result = result.to_dict(orient='records')[0]
        result = {'result' : result}
        result['result']['previous_object_id'] = request.session['previous_object_id']
        
        # get total label count:
        count_query = web_app_queries['SELECT_get_total_labels']
        count_parameters = {
            'user_id' : request.user.email,
        }
        count_result = PostgresCaller.main(count_query, count_parameters, **kwargs)
        count = int(count_result.iloc[0]) 
        result['result']['count'] = count
       
        print()
        print('[GET]--[NEXT]--[START]')
        print('[GET]--[NEXT]--[PARAMETERS] (no paramters for get next view)')
        print(parameters)
        print()
       
        # set view to in use:
        parameters = {
            'object_id' : result['result']['object_id'],
            'previous_object_id' : request.session['previous_object_id'],
        }
        query_file = web_app_queries['UPDATE_set_view_to_in_use']
        PostgresCaller.main(query_file, parameters, **kwargs)
       
        print('[GET]--[NEXT]--[PARAMETERS] (parameters to set view to "in use")')
        print(parameters)
        print()
        print('[GET]--[NEXT]--[RESULT] (data pulled from database with these values)')
        print(result)
        print()
        print('[GET]--[NEXT]--[END]')
    
    return render(request, template_name='validator.html', context=result)
