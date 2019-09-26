import os
from time import time
import Tools.ProductionTools as tools
import Components.SegmentationApical.SegmentationApicalFunctions as funcs



def main(file_paths, verbose=False, start=time()):
    
    # Unpack files:
    videos_directory = file_paths['videos_directory']
    views_data_file = file_paths['views_table']
    configuration_file = file_paths['segmentation_model_apical_configuration']
    export_file = file_paths['segmentation_apical_table']
    a4c_model = file_paths['a4c_segmentation_model']
    a2c_model = file_paths['a2c_segmentation_model']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Step 2, read views data from file:
    views_data = tools.ReadDataFromFile(views_data_file, verbose, start)
    
    # Step 3, parse views data:
    a4c_views_data = funcs.ParseViewsData(views_data, 'A4C', videos_directory, verbose, start)
    a2c_views_data = funcs.ParseViewsData(views_data, 'A2C', videos_directory, verbose, start)
    
    # Step 4, prepare segmentation model:
    segmentration_metrics = funcs.PrepSegmentationModel(configuration_file, verbose, start)
    
    # Step 5, predict segmentation:
    a4c_segmentation = funcs.PredictSegmentation(a4c_views_data, a4c_model, segmentration_metrics, verbose, start)
    a2c_segmentation = funcs.PredictSegmentation(a2c_views_data, a2c_model, segmentration_metrics, verbose, start)
    
    # Step 6, process model results:
    a4c_segmentation_data = funcs.ProcessSegmentationResults(a4c_segmentation, 'A4C', verbose, start)
    a2c_segmentation_data = funcs.ProcessSegmentationResults(a2c_segmentation, 'A2C', verbose, start)
    
    # Step 7, merge data:
    a4c_segmentation_data = tools.JoinDataFrames(a4c_views_data, a4c_segmentation_data, 'dicom_id', verbose, start)
    a2c_segmentation_data = tools.JoinDataFrames(a2c_views_data, a2c_segmentation_data, 'dicom_id', verbose, start)
    segmentation_data = tools.ConcatDataFrames(a4c_segmentation_data, a2c_segmentation_data, verbose, start)
    
    # Step 8, export data:
    tools.ExportDataToFile(segmentation_data, export_file, verbose, start)
