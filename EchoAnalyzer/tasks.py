from Pipeline.ProductionPipeline import ProductionPipeline
from EchoAnalyzer.models import File, Visit
from datetime import datetime, timezone
from WebTools.Tools import PrintTitle
from django.http import HttpResponse
from django.shortcuts import render
from multiprocessing import Pool
from django.urls import reverse
from time import time, sleep
import traceback
import json
import sys



def ProcessVisit(user_id, visit_id):

    ''' Accepts a user_id, visit_id, processes all files for that visit + user '''
    
    PrintTitle('EchoAnalyzer.tasks.ProcessVisit')
    
    visit = Visit.objects.get(pk=visit_id)
    
    # set start processing time:
    visit.started_processing_at = datetime.now(timezone.utc)
    visit.save()
    
    # get list of files associated to visit:
    file_list = list(visit.file_set.all().values_list('id', flat=True))
    
    # get number of threads:
    number_of_threads = len(file_list)
    
    # create pool:
    pool = Pool(number_of_threads)
    
    # set up array for multiprocessing:
    multiprocess_input = []

    # file pipeline preprocessing:
    for file_id in file_list:
        
        # get file object:
        file = File.objects.get(pk=file_id)
        file_name = file.file_name
        dicom_id = file.dicom_id
        
        # set start processing time:
        file.started_processing_at = datetime.now(timezone.utc)
        file.save()
    
        input_point = {'user_id':user_id, 'visit_id':visit_id, 'file_id':file_id, 'dicom_id':dicom_id, 'file_name':file_name}
        
        print('[EchoAnalyzer.tasks.ProcessVisit]: input [%s]' %input_point)

        multiprocess_input.append(input_point)
    
    # multiprocess:
    result_json_list = pool.map(ProductionPipeline, multiprocess_input)
    
    # file pipeline post processing:
    for file_id in file_list:
        
        # get file object:
        file = File.objects.get(pk=file_id)
        
        # set finish processing time, log:
        file.finished_processing_at = datetime.now(timezone.utc)
        
        # get log:
        for result_json in result_json_list:
            
            if result_json['file_id'] == file.id: 
        
                with open(result_json['reports']['log'], 'r') as log:
                    file.log = log.read()
        
        file.save()
    
    # pack result list as json:
    result_json = {'result' : result_json_list}
    
    # set completed processing time and save results:
    
    visit.finished_processing_at = datetime.now(timezone.utc)
    visit.results = result_json
    visit.save()
    
    
    return result_json