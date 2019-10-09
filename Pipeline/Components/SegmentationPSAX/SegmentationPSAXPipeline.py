import os
from time import time
import Tools.ProductionTools as tools
import Components.SegmentationPSAX.SegmentationPSAXFunctions as funcs



def main(file_paths, psax_seg_model, verbose=False, start=time()):
    
    # Unpack files:
    videos_directory = file_paths['videos_directory']
    views_data_file = file_paths['views_table']
    # configuration_file = file_paths['segmentation_model_psax_configuration']
    export_file = file_paths['segmentation_psax_table']
    # psax_model = file_paths['psax_model']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Step 2, read views data from file:
    views_data = tools.ReadDataFromFile(views_data_file, verbose, start)
    
    # Step 3, parse views data:
    psax_views_data = funcs.ParseViewsData(views_data, 'PSAX', videos_directory, verbose, start)
    
    # # Step 4, prepare segmentation model:
    # segmentation_metrics = funcs.PrepSegmentationModel(configuration_file, verbose, start)
    
    # Step 5, predict segmentation:
    psax_segmentation = funcs.PredictSegmentation(psax_views_data, verbose, start)
    
    # Step 6, process model results:
    psax_segmentation_data = funcs.ProcessSegmentationResults(psax_segmentation, 'PSAX', verbose, start)
    
    # Step 7, merge data:
    psax_segmentation_data = tools.JoinDataFrames(psax_views_data, psax_segmentation_data, 'dicom_id', verbose, start)
       
    # Step 8, export data:
    tools.ExportDataToFile(psax_segmentation_data, export_file, verbose, start)
