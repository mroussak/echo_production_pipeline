from Components.Views import ViewsFunctions as funcs



def ViewsPipeline(file_paths):
    
    # unpack files:
    dicom_id = file_paths['dicom_id']
    dicom_data_destination = file_paths['dicom_data']
    view_data_destination = file_paths['view_data']
    
    print('\n[ViewsPipeline]__')
    
    # Step 1, Download file from s3:
    dicom = funcs.GetDicomData(dicom_data_destination)
    
    # Step 2, get prediction:
    #prediction = funcs.GetPrediction(dicom)
    prediction = funcs.GetPredictionVideoLevel(dicom)
    
    # Step 3, parse prediction:
    #parsed_prediction = funcs.ParsePrediction(dicom_id, prediction)
    parsed_prediction = funcs.ParsePredictionVideoLevel(dicom_id, prediction)
    
    # Step 4, export prediction:
    funcs.ExportPrediction(parsed_prediction, view_data_destination)