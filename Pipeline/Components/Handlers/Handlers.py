from Configuration.Configuration import configuration
from Tools import Tools
import importlib
import sys
import os



def Initializer(file_paths):
    
    ''' Accepts file_paths, builds directories and reroutes stdout to log file '''
    
    # Reload tools module (resets timer):
    importlib.reload(Tools)
    
    # Build file paths:
    for file_path in [
        file_paths['DATA_DIR'],
        file_paths['DICOMS_DIR'],
        file_paths['MEDIA_DIR'],
        file_paths['REPORTS_DIR'],
        file_paths['dicom_jpegs'],
        ]:
    
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    
    # Send stdout to log file:
    if configuration['handlers']['log']:
        sys.stdout = open(file_paths['log_file'], 'w+')
        print(
            '[ProductionPipeline]__ User ID [%s]; Visit ID [%s]; File ID [%s], Dicom ID[%s], File Name [%s];' 
            %(file_paths['user_id'], file_paths['visit_id'], file_paths['file_id'], file_paths['dicom_id'], file_paths['file_name'])
            )
    else:
        sys.stdout = sys.__stdout__
        


def Terminator():
    
    ''' Reroutes stdout back to terminal '''
    
    sys.stdout = sys.__stdout__
    
    