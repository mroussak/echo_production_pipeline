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
import shutil
import json
import sys



def FilePipelinePreprocessing(user_id, visit_id, file_list):

    # initialize variables:
    multiprocess_input = []
    
    # file pipeline preprocessing:
    for file_id in file_list:
        
        # get file object, start timer:
        file = File.objects.get(pk=file_id)
        file_name = file.file_name
        dicom_id = file.dicom_id
        file.started_processing_at = datetime.now(timezone.utc)
        file.save()
    
        # create input point, append to list:
        input_point = {'user_id':user_id, 'visit_id':visit_id, 'file_id':file_id, 'dicom_id':dicom_id, 'file_name':file_name}
        multiprocess_input.append(input_point)
        
        # debug:
        print('[EchoAnalyzer.tasks.ProcessVisit]: input [%s]' %input_point)
    
    return multiprocess_input



def FilePipelinePostprocessing(user_id, visit_id, file_list):
    
    # initialize variables:
    result_json_list = []
    
    # file pipeline post processing:
    for file_id in file_list:
        
        # get file object:
        file = File.objects.get(pk=file_id)
        dicom_id = file.dicom_id
        
        # get result json file path:
        BASE_DIR = '/tmp/WebAppData/Users/' + str(user_id) + '/Visits/' + str(visit_id) + '/Files/' + str(file_id) + '/'
        REPORTS_DIR = BASE_DIR + 'Reports/'
        JSON_FILE = REPORTS_DIR + dicom_id + '_report.json'
        
        # get result_json:
        with open(JSON_FILE, 'r') as handle:
            result_json = json.load(handle)
        
        # get log:
        with open(result_json['reports']['log'], 'r') as log:
            file.log = log.read()
        
        # set finish processing time:
        file.finished_processing_at = datetime.now(timezone.utc)
        file.processing_time = datetime.now(timezone.utc) - file.started_processing_at
        file.save()
        
        # append result_json to list for visit object:
        result_json_list.append(result_json)
    
    return result_json_list



def ProcessVisit(user_id, visit_id):

    ''' Accepts a user_id, visit_id, processes all files for that visit + user '''
    
    PrintTitle('EchoAnalyzer.tasks.ProcessVisit')
    
    # initialize variables:
    multiprocess_input = []
    result_json_list = []
    
    # get visit by id, start timer:
    visit = Visit.objects.get(pk=visit_id)
    visit.started_processing_at = datetime.now(timezone.utc)
    visit.save()
    
    # get list of files associated to visit:
    file_list = list(visit.file_set.all().values_list('id', flat=True))
    
    # set up multiprocessing pool:
    number_of_threads = len(file_list)
    pool = Pool(number_of_threads)
    
    # file preprocessing:
    multiprocess_input = FilePipelinePreprocessing(user_id, visit_id, file_list)

    # multiprocess:
    pool.map(ProductionPipeline, multiprocess_input)
    
    # file postprocessing:
    result_json_list = FilePipelinePostprocessing(user_id, visit_id, file_list)
        
    # delete existing temp data off of server:
    #shutil.rmtree(result_json_list[0]['VISIT_DIR'])
    
    # pack result list as json:
    results = {'results' : result_json_list}
    
    # set completed processing time and save results:
    visit.finished_processing_at = datetime.now(timezone.utc)
    visit.processing_time = datetime.now(timezone.utc) - visit.started_processing_at
    visit.results = results
    visit.save()
