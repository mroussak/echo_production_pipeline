import sys
import os



def Initializer(file_paths, log=True):
    
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
    if log:
        sys.stdout = open(file_paths['log_file'], 'w+')
    
    print('[ProductionPipeline]__ User ID [%s]; Visit ID [%s]; Dicom ID [%s];' %(file_paths['user_id'], file_paths['visit_id'], file_paths['dicom_id']))