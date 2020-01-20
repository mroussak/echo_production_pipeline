from Pipeline.Configuration.Configuration import configuration
from Pipeline.Tools import Tools as tools
from datetime import datetime
from decouple import config
import importlib
import shutil
import boto3
import sys
import os



def Initializer(file_paths):
    
    ''' Accepts file_paths, builds directories and reroutes stdout to log file '''
    
    # Reload tools module (resets timer):
    importlib.reload(tools)
    
    # Build file paths:
    for file_path in [
        file_paths['DATA_DIR'],
        file_paths['DICOMS_DIR'],
        file_paths['MEDIA_DIR'],
        file_paths['REPORTS_DIR'],
        file_paths['dicom_jpegs'],
        ]:
    
        # create directories + files:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    
    open(file_paths['log_file'],'w+')
    
    # Send stdout to log file:
    if configuration['handlers']['log']:
        
        sys.stdout = open(file_paths['log_file'], 'w+')
    
    print(
        '[ProductionPipeline]__ User ID [%s]; Visit ID [%s]; File ID [%s], Dicom ID[%s], File Name [%s];' 
        %(file_paths['user_id'], file_paths['visit_id'], file_paths['file_id'], file_paths['dicom_id'], file_paths['file_name'])
        )
        
    

def Terminator(file_paths):
    
    ''' Reroutes stdout back to terminal, moves artifacts to s3 and deletes them on current instance '''
   
    # get bucket name:
    BUCKET_NAME = config('AWS_S3_BUCKET_NAME')

    # connect to s3:
    client = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'), aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
    s3 = boto3.resource('s3')
   
    # iterate over each file in base directory:
    for path, subdirs, files in os.walk(file_paths['BASE_DIR']):
        for name in files:
            
            # skip uploading pkl files:
            if name[-3:] == 'pkl':
                continue
            
            # get the file to be exported:
            local_file = os.path.join(path, name)
            s3_destination = local_file.replace('/tmp/','tmp/')
           
            # write to bucket:
            s3.Bucket(BUCKET_NAME).upload_file(local_file, s3_destination)
    
    # reroute stdout back to console:        
    sys.stdout = sys.__stdout__
    
    