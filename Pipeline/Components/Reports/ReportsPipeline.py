import Components.Reports.ReportsFunctions as funcs
import Tools.ProductionTools as tools
from time import time
import os



def main(file_paths, verbose=False, start=time()):

    # Unpack files:
    views_data_file = file_paths['views_table']
    segmentation_apical_data_file = file_paths['segmentation_apical_table']
    segmentation_psax_data_file = file_paths['segmentation_psax_table']
    export_file = file_paths['reports']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)

    # Step 2, read data from file:
    views_data = tools.ReadDataFromFile(views_data_file, verbose, start)
    segmentation_apical_data = tools.ReadDataFromFile(segmentation_apical_data_file, verbose, start)
    segmentation_psax_data = tools.ReadDataFromFile(segmentation_psax_data_file, verbose, start)
    
    # Step 3, parse data:
    views_data = funcs.ParseViewsData(views_data, verbose, start)
    segmentation_apical_data = funcs.ParseSegmentationApicalData(segmentation_apical_data, verbose, start)
    segmentation_psax_data = funcs.ParseSegmentationPSAXData(segmentation_psax_data, verbose, start)
    
    # Step 4, append data:
    reports_data = tools.ConcatDataFrames(segmentation_apical_data, segmentation_psax_data, 'reports_data', verbose, start)
    
    # Step 5, build gifs, resize videos:
    #funcs.ResizeVideos(reports_data, verbose, start) # decided to not resize videos presently
    funcs.BuildGifs(views_data, verbose, start)

    
    # Step 6, build json:
    reports_json = funcs.BuildJsonFromData(reports_data, verbose, start)
    
    # Step 7, export json:
    tools.ExportDataToFile(reports_json, export_file, verbose, start)
