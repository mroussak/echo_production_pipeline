import Tools.DatabaseTools as tools
from time import time, sleep
import pandas as pd
import hashlib
import sys
import os

# Database imports:
#sys.path.insert(1, '/internal_drive/echo_production_pipeline/Database/EchoData/')
sys.path.insert(1, '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/')
import PostgresCaller



@tools.time_it(**tools.kwargs)
def PrepVideosTable(videos_table):
    
    ''' Accepts videos table, returns prepped videos table '''
    
    return videos_table
    
    
    
@tools.time_it(**tools.kwargs)
def PrepManuallyAddedDataTable(manually_added_data_table):
    
    ''' Accepts manually added data table table, returns prepped manually added data table table '''

    # drop unused columns:    
    manually_added_data_table = manually_added_data_table.drop(columns = 'path_to_jpegs')

    # parse video names:
    manually_added_data_table['path_to_dicom_webm'] = manually_added_data_table['path_to_dicom_webm'].str.split('/', expand=True)[3]
    
    return manually_added_data_table
    
    

@tools.time_it(**tools.kwargs)
def PopulateVideosTable(videos_table, vidoes_table_query):

    ''' Accepts videos table, populates database '''
    
    for index, row in videos_table.iterrows():
        
        try:
        
            # build parameters:
            parameters = {
                'object_id' : row['object_id'],
                'path_to_jpegs' : row['path_to_jpegs'],
                'patient_hash' : row['patient_hash'],
                'visit_date' : row['visit_date'],
                'folder' : row['folder'],
            }
        
            # populate database:
            PostgresCaller.main(vidoes_table_query, parameters)
    
        except:
            pass
    
    

@tools.time_it(**tools.kwargs)
def PopulateManuallyAddedDataTable(manually_added_data_table, manually_added_data_table_query):
    
    ''' Accepts manually added data table table table, populates database '''
    
    for index, row in manually_added_data_table.iterrows():
        
        try:
        
            parameters = {
                'object_id' : row['object_id'],
                'video_id' : row['video_id'],
                'path_to_dicom_webm' : row['path_to_dicom_webm'],
            }
        
            # populate database:
            PostgresCaller.main(manually_added_data_table_query, parameters)
    
        except:
            pass