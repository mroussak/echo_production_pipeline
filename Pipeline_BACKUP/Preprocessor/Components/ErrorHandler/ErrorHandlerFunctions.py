from time import time
import numpy as np



def ProcessDicomError(dicom, statuses, verbose=False, start=time()):
    
    ''' Accepts dicom object, returns status object with error codes '''
    
    # intialize variables:
    dicom_status = {
        'status_code' : 0,
        'status_label' : statuses[0],
        'missing_elements' : [],
    }
    
    # warnings (non-fatal missing fields):
    for key in ['manufacturer', 'manufacturer_model_name']:
        if dicom[key] == None:
            dicom_status['status_code'] = 1
            dicom_status['status_label'] = statuses[1]
            dicom_status['missing_elements'].append(key)
    
    # errors (fatal missing fields):
    for key in ['physical_units_x_direction', 'physical_units_y_direction', 'physical_delta_x', 'physical_delta_y', 'dicom_type', 'number_of_frames']:
        if dicom[key] == None:
            dicom_status['status_code'] = 2
            dicom_status['status_label'] = statuses[2]
            dicom_status['missing_elements'].append(key)
    
    # pixel data error (fata missing field):
    if type(dicom['pixel_data']) != np.ndarray:
        dicom_status['status_code'] = 2
        dicom_status['status_label'] = statuses[2]
        dicom_status['missing_elements'].append(key)
        
    if verbose:
        print('[@ %7.2f s] [ProcessDicomError]: Processed dicom error with status code [%s]' %(time()-start, dicom_status['status_code']))
        
    return dicom_status
    
    
    
def CompileErrorStauses(dicom_file_path, dicom_status, anonymizer_status, normalizer_status, verbose=False, start=time()):
    
    ''' Accepts status objects, returns compiled status object '''
    
    # intialize variables:
    status = {
        'dicom_file_path' : dicom_file_path,
        'status_code' : dicom_status['status_code'],
        'status_label' : dicom_status['status_label'],
        'missing_elements' : dicom_status['missing_elements'],
    }
    
    if verbose:
        print('[@ %7.2f s] [CompileErrorStauses]: Compiled statuses' %(time()-start))
        
    return status