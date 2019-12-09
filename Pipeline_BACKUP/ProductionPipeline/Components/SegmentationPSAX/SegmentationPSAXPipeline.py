import Components.SegmentationPSAX.SegmentationPSAXFunctions as funcs
import Tools.ProductionTools as tools
from time import time
import os



def main(file_paths, verbose=False, start=time()):

    # Unpack files:
    videos_directory = file_paths['videos_directory']
    views_data_file = file_paths['views_table']
    export_file = file_paths['segmentation_psax_table']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)

    # Step 2, read views data from file:
    views_data = tools.ReadDataFromFile(views_data_file, verbose, start)
    
    # Step 3, parse views data:
    psax_views_data = funcs.ParseViewsData(views_data, 'PSAX', videos_directory, verbose, start)
    
    # Step 4, predict segmentation:
    psax_segmentation = funcs.PredictSegmentation(psax_views_data, verbose, start)
    
    # Step 5, process model results:
    psax_segmentation_data = funcs.ProcessSegmentationResults(psax_segmentation, 'PSAX', verbose, start)
    
    # Step 6, merge data:
    psax_segmentation_data = tools.JoinDataFrames(psax_views_data, psax_segmentation_data, 'dicom_id', 'psax_segmentation_data', verbose, start)
       
    # Step 7, export data:
    tools.ExportDataToFile(psax_segmentation_data, export_file, verbose, start)
