from Components.DicomExtractor import DicomExtractor 
from Components.ErrorHandler import ErrorHandler
import Tools.PreprocessorTools as tools
from time import time
import os



def main(dicom_file, verbose=False, start=time()):
    
    # Variables:
    kwargs = {
        'verbose' : verbose,
        'start' : start,
    }
    
    # Step 1, DicomExtractor:
    dicom = DicomExtractor.main(dicom_file, **kwargs)
    
    # Step 2, Anonymizer:
    #TODO
    
    # Step 3, Normalizer:
    #TODO
    
    # Step 5, ErrorHandler:
    status = ErrorHandler.main(dicom_file, dicom, **kwargs)
    
    # Step 4, export dicom:
    return tools.ExportDicom(dicom, status, **kwargs)
    
