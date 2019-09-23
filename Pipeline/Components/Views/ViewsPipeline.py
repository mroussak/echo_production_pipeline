import os
from time import time
import Tools.ProductionTools as tools
import Components.Views.ViewsFunctions as funcs



def main(file_paths, verbose=False, start=time()):

    # Unpack files:
    dicom_data_file = file_paths['dicoms_table']
    export_file = file_paths['views_table']
    model = file_paths['views_model']
    unique_views = ['A2C', 'A3C', 'A4C', 'A5C', 'PLAX', 'PSAX', 'PSAXA', 'RVIT', 'SUBA', 'SUBB', 'SUPA']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)
        
    # Step 2, read dicom data from file:
    dicom_data = tools.ReadDataFromFile(dicom_data_file, verbose, start)
    
    # Step 3, parse dicom data:
    dicom_data = funcs.ParseDicomData(dicom_data, verbose, start)
    
    # Step 4, predict view for each video:
    predictions = funcs.PredictViews(dicom_data, model, verbose, start)
    
    # Step 5, process model results:
    predictions = funcs.ProcessViewsPredictions(predictions, verbose, start)
    
    # Step 6, merge predictions to dicom_data:
    dicom_data = tools.JoinDataFrames(dicom_data, predictions, "dicom_id", verbose, start)
    
    # Step 7, export data:
    tools.ExportDataToFile(dicom_data, export_file, verbose, start)