from Pipeline.Configuration.Configuration import configuration
from Pipeline.Components.Media import MediaFunctions as funcs
from Pipeline.Tools import Tools as tools



def MediaPipeline(file_paths):
    
    # unpack file paths:
    MEDIA_DIR = file_paths['MEDIA_DIR']
    dicom_file = file_paths['dicom_data']
    jpeg_destintation = file_paths['dicom_jpegs']
    gif_destination = file_paths['dicom_gif']
    mp4_destination = file_paths['dicom_mp4']
    webm_destination = file_paths['dicom_webm']
    
    print('\n[MediaPipeline]__')
    
    # Step 1, get dicom data:
    dicom = funcs.GetDicomData(dicom_file)
    
    # Step 2, build media base directory:
    funcs.BuildMediaBaseDirectory(MEDIA_DIR)
    
    # Step 3, build video:
    #funcs.BuildMP4(dicom, mp4_destination)
    funcs.BuildWebm(dicom, webm_destination) ## 1 minute processing time