from Components.Views import ViewsFunctions as funcs
from Configuration.Configuration import configuration
from Tools import Tools as tools



def ViewsPipeline(file_paths):
    
    # unpack files:
    dicom_id = file_paths['dicom_id']
    destination_directory = file_paths['downloads']
    dicom_data_destination = file_paths['dicom_data']
    view_data_destination = file_paths['view_data']
    
    print('\n[ViewsPipeline]__')
    
    # Step 1, Download file from s3:
    dicom = funcs.GetDicomData(dicom_data_destination)
    
    # Step 2, get prediction:
    prediction = funcs.GetPrediction(dicom)
    
    # Step 3, parse prediction:
    parsed_prediction = funcs.ParsePrediction(dicom_id, prediction)
    
    funcs.ExportPrediction(parsed_prediction, view_desti)
    funcs.ExportPrediction(parsed_prediction, view_data_destination)