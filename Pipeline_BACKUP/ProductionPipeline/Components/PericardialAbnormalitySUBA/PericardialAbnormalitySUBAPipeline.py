import Components.PericardialAbnormalitySUBA.PericardialAbnormalitySUBAFunctions as funcs
import Tools.ProductionTools as tools
from time import time
import os


def main(file_paths, verbose=False, start=time()):

    # Unpack files:
    videos_directory = file_paths['videos_directory']
    views_data_file = file_paths['views_table']
    export_file = file_paths['pericardial_abnormality_suba_table']

    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
    
    # Step 2, read views data from file:
    views_data = tools.ReadDataFromFile(views_data_file, verbose, start)
    
    # Step 3, parse views data:
    suba_views_data = funcs.ParseViewsData(views_data, 'SUBA', videos_directory, verbose, start)
    
    # Step 4, predict pericardial abnormalities:
    suba_predictions = funcs.PredictPericardialAbnormality(suba_views_data, verbose, start)

    # Step 5, process model results:
    suba_predictions_data = funcs.ProcessPericardialAbnormalityResults(suba_predictions, verbose, start)
    
    # Step 6, merge data:
    suba_predictions_data = tools.JoinDataFrames(suba_views_data, suba_predictions_data, 'dicom_id', 'suba_predictions_data', verbose, start)
    
    # Step 7, export data:
    tools.ExportDataToFile(suba_predictions_data, export_file, verbose, start)