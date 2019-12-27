from Pipeline.Configuration.Configuration import configuration
from Pipeline.Components.Segmentation import SegmentationFunctions as funcs
from Pipeline.Tools import Tools as tools



def SegmentationPipeline(file_paths):
    
    # unpack file paths:
    dicom_data = file_paths['dicom_data']
    view_data = file_paths['view_data']
    segmentation_data_destination = file_paths['segmentation_data']
    
    print('\n[SegmentationPipeline]__')
    
    # Step 1, get dicom, view data:
    dicom = funcs.GetData(dicom_data)
    view = funcs.GetData(view_data)
    
    # Step 2, prep data for model:
    prepped_data = funcs.PrepDataForModel(dicom, view)
    
    # Step 3, get prediction:
    prediction = funcs.GetPrediction(prepped_data)
    
    # Step 4, parse prediction:
    segmentation_data = funcs.ParsePrediction(prediction)
    
    # Step 5, export segmentation data:
    funcs.ExportSegmentationData(segmentation_data, segmentation_data_destination)