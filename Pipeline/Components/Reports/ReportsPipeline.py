import os
from time import time
import Tools.ProductionTools as tools
import Components.Reports.ReportsFunctions as funcs



def main(file_paths, verbose=False, start=time()):
    
    # Unpack files:
    segmentation_data_file = file_paths['segmentation_table']
    export_file = file_paths['reports']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Step 2, read segmentation data from file:
    segmentation_data = tools.ReadDataFromFile(segmentation_data_file, verbose, start)
    
    # Step 3, parse segmentation data:
    segmentation_data = funcs.ParseSegmentationData(segmentation_data, verbose, start)
    
    # Step 4, build json:
    reports_json = funcs.BuildJsonFromData(segmentation_data, verbose, start)
    
    # Step 4, export json:
    tools.ExportDataToFile(reports_json, export_file, verbose, start)
