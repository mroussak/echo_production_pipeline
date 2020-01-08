from Pipeline.Components.Segmentation import SegmentationFunctions as funcs
from Pipeline.Tools import Tools as tools



@funcs.am_i_apical()
def SegmentationPipeline(file_paths):
    
    # unpack file paths:
    dicom_data = file_paths['dicom_data']
    view_data = file_paths['view_data']
    segmentation_data_destination = file_paths['segmentation_data']
    simpsons_data_destination = file_paths['simpsons_data']
    
    print('\n[SegmentationPipeline]__')
    
    # Step 1, get dicom, view data:
    dicom = funcs.GetData(dicom_data)
    
    # Step 2, prep data for model:
    prepped_data = funcs.PrepDataForModel(dicom)
    
    # Step 3, get prediction:
    prediction = funcs.GetPrediction(prepped_data)
    
    # Step 4, parse prediction:
    parsed_prediction = funcs.ParsePrediction(dicom, prediction)
    
    # Step 5, export segmentation data:
    funcs.ExportSegmentationData(parsed_prediction, segmentation_data_destination, simpsons_data_destination)