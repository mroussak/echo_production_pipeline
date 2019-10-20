import Components.ErrorHandler.ErrorHandlerFunctions as funcs
from time import time



def main(dicom_file_path, dicom, verbose=False, start=time()):
    
    # Variables:
    statuses = {
        0: '[clear]: no errors',
        1: '[warning]: non-fatal missing field',
        2: '[error]: fatal missing field',
    }
    
    kwargs = {
        'verbose' : verbose,
        'start' : start,
    }
    
    # Step 1, process dicom error:    
    dicom_status = funcs.ProcessDicomError(dicom, statuses, **kwargs)
    
    # Step 2, process anonymizer error:
    anonymizer_status = None # TODO
    
    # Step 3, process normalizer error:
    normalizer_status = None # TODO
    
    # Step 4, compile errors:
    status = funcs.CompileErrorStauses(dicom_file_path, dicom_status, anonymizer_status, normalizer_status, **kwargs)
    
    # Step 5, export status:
    return status