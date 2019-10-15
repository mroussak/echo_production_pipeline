import Components.SegmentationApical.SegmentationApicalFunctions as funcs
import Tools.ProductionTools as tools
from time import time
import os



def main(file_paths, verbose=False, start=time()):


    # Unpack files:
    videos_directory = file_paths['videos_directory']
    views_data_file = file_paths['views_table']
    export_file = file_paths['segmentation_apical_table']

    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Step 2, read views data from file:
    views_data = tools.ReadDataFromFile(views_data_file, verbose, start)
    
    # Step 3, parse views data:
    a4c_views_data = funcs.ParseViewsData(views_data, 'A4C', videos_directory, verbose, start)
    a2c_views_data = funcs.ParseViewsData(views_data, 'A2C', videos_directory, verbose, start)
    
    # Step 4, predict segmentation:
    a4c_segmentation = funcs.PredictSegmentation(a4c_views_data, 'A4C', verbose, start)
    a2c_segmentation = funcs.PredictSegmentation(a2c_views_data, 'A2C', verbose, start)
    
    # Step 5, process model results:
    a4c_segmentation_data = funcs.ProcessSegmentationResults(a4c_segmentation, 'A4C', verbose, start)
    a2c_segmentation_data = funcs.ProcessSegmentationResults(a2c_segmentation, 'A2C', verbose, start)
    
    # Step 6, merge data:
    a4c_segmentation_data = tools.JoinDataFrames(a4c_views_data, a4c_segmentation_data, 'dicom_id', 'a4c_segmentation_data', verbose, start)
    a2c_segmentation_data = tools.JoinDataFrames(a2c_views_data, a2c_segmentation_data, 'dicom_id', 'a2c_segmentation_data', verbose, start)
    segmentation_data = tools.ConcatDataFrames(a4c_segmentation_data, a2c_segmentation_data, 'segmentation_data', verbose, start)
    
    # Step 7, export data:
    tools.ExportDataToFile(segmentation_data, export_file, verbose, start)
