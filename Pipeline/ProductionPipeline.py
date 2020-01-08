#!/usr/bin/env python
from Pipeline.Components.Segmentation.SegmentationPipeline import SegmentationPipeline
from Pipeline.Components.Handlers.Handlers import Initializer, Terminator
from Pipeline.Components.Reports.ReportsPipeline import ReportsPipeline
from Pipeline.Components.Dicoms.DicomsPipeline import DicomsPipeline
from Pipeline.Components.Views.ViewsPipeline import ViewsPipeline
from Pipeline.Components.Media.MediaPipeline import MediaPipeline
import json



def ProductionPipeline(input_dictionary):
    
    # unpack input dictionary:
    user_id = input_dictionary['user_id']
    visit_id = input_dictionary['visit_id']
    file_id = input_dictionary['file_id']
    dicom_id = input_dictionary['dicom_id']
    file_name = input_dictionary['file_name']
    
    # build base directories:
    USER_DIR = '/tmp/WebAppData/Users/' + str(user_id) + '/'
    VISIT_DIR = '/tmp/WebAppData/Users/' + str(user_id) + '/Visits/' + str(visit_id) + '/'
    FILE_DIR =  '/tmp/WebAppData/Users/' + str(user_id) + '/Visits/' + str(visit_id) + '/Files/' + str(file_id) + '/'
    
    BASE_DIR = '/tmp/WebAppData/Users/' + str(user_id) + '/Visits/' + str(visit_id) + '/Files/' + str(file_id) + '/'
    DATA_DIR = BASE_DIR + 'Data/'
    DICOMS_DIR = BASE_DIR + 'Dicoms/'
    MEDIA_DIR = BASE_DIR + 'Media/'
    REPORTS_DIR = BASE_DIR + 'Reports/'
    
    file_paths = {
        
        # ids:
        'user_id' : user_id,
        'visit_id' : visit_id,
        'file_id' : file_id,
        'dicom_id' : dicom_id,
        'file_name' : file_name,
        
        # roots:
        'USER_DIR' : USER_DIR,
        'VISIT_DIR' : VISIT_DIR,
        'FILE_DIR' : FILE_DIR,
        'BASE_DIR' : BASE_DIR,
        'DATA_DIR' : DATA_DIR,
        'DICOMS_DIR' : DICOMS_DIR,
        'MEDIA_DIR' : MEDIA_DIR,
        'REPORTS_DIR' : REPORTS_DIR,
        
        # data:
        'dicom_data' : DATA_DIR + dicom_id + '_dicom.pkl',
        'view_data' : DATA_DIR + dicom_id + '_view.pkl',
        'segmentation_data' : DATA_DIR + '_segmentation.pkl',
        'simpsons_data' : DATA_DIR + '_simpsons.pkl',
        
        # media:
        'dicom_jpegs' : MEDIA_DIR + '/Jpegs/',
        'dicom_avi' : MEDIA_DIR + dicom_id +'.avi',
        'dicom_gif' : MEDIA_DIR + dicom_id +'.gif',
        'dicom_mp4' : MEDIA_DIR + dicom_id + '.mp4',
        'dicom_webm' : MEDIA_DIR + dicom_id + '.webm',
        'segmentation_webm' : MEDIA_DIR + dicom_id + '_segmentation.webm',
        'simpsons_webm' : MEDIA_DIR + dicom_id + '_simpsons.webm',
        
        # reports:
        'reports_json' : REPORTS_DIR + dicom_id + '_report.json',
        'log_file' : REPORTS_DIR + dicom_id + '_log.txt',
    }
    
    # Step 0) Initializer:
    Initializer(file_paths)
    
    # Step 1) Dicom Pipeline:
    DicomsPipeline(file_paths)
    
    # Step 2) Views Pipeline:
    ViewsPipeline(file_paths)

    # Step 4) Segmentation Pipeline:
    SegmentationPipeline(file_paths)
    
    # Step 5) Media Pipeline:
    MediaPipeline(file_paths)

    # Step 6) Reports Pipeline:
    ReportsPipeline(file_paths)

    # Step 7) Terminator:
    Terminator(file_paths)
    


if __name__ == '__main__':    

    s3_files = ['test1', 'test2', 'test3', 'test4', 'test5']

    for dicom_id in s3_files:
        
        input_data = {
            'user_id' : 'daniel@icardio.ai',
            'visit_id' : 2,
            'file_id' : dicom_id,
            'dicom_id' : dicom_id,
            'file_name' : dicom_id,
        }
        
        ProductionPipeline(input_data)
        