import os
from time import time
import Tools.ProductionTools as tools
import Components.Reports.ReportsFunctions as funcs



def main(file_paths, verbose=False, start=time()):
    
    # Unpack files:
    segmentation_apical_data_file = file_paths['segmentation_apical_table']
    segmentation_psax_data_file = file_paths['segmentation_psax_table']
    export_file = file_paths['reports']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Step 2, read segmentation data from file:
    segmentation_apical_data = tools.ReadDataFromFile(segmentation_apical_data_file, verbose, start)
    segmentation_psax_data = tools.ReadDataFromFile(segmentation_psax_data_file, verbose, start)
    
    # Step 3, parse segmentation data:
    segmentation_apical_data = funcs.ParseSegmentationApicalData(segmentation_apical_data, verbose, start)
    segmentation_psax_data = funcs.ParseSegmentationPSAXData(segmentation_psax_data, verbose, start)
    
    # Step 4, append data:
    reports_data = tools.ConcatDataFrames(segmentation_apical_data, segmentation_psax_data, verbose, start)
    
    # Step 5, resize videos:
    funcs.ResizeVideos(reports_data, verbose, start)
    
    # Step 6, build json:
    reports_json = funcs.BuildJsonFromData(reports_data, verbose, start)
    
    # Step 7, export json:
    tools.ExportDataToFile(reports_json, export_file, verbose, start)
