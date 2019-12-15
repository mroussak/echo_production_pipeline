import Components.Dicoms.DicomsFunctions as funcs
import Tools.ProductionTools as tools
from time import time
import pandas as pd
import os



def main(file_paths, verbose=False, start=time()):

    # Unpack files:
    dicoms_directory = file_paths['dicoms_directory']
    videos_directory = file_paths['dicoms_videos_directory']
    dicom_data_file = file_paths['dicoms_table']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)

    # Step 2, read dicoms:
    dicoms = funcs.ReadDicoms(dicoms_directory, verbose, start)

    # Step 3, parse dicoms:
    dicom_data, pixel_array_data = funcs.ParseDicoms(dicoms, videos_directory, verbose, start)
    # pixel_array_data = funcs.AnonymizeDicoms(pixel_array_data, verbose, start) #TODO

    # Step 4, build videos, gifs:
    funcs.BuildVideos(pixel_array_data, verbose, start)
    
    # Step 5, export dicoms:
    tools.ExportDataToFile(dicom_data, dicom_data_file, verbose, start)
