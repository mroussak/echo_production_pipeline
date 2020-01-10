from Pipeline.Configuration.Configuration import configuration
from Pipeline.Components.Media import MediaFunctions as funcs
from Pipeline.Tools import Tools as tools



def MediaPipeline(file_paths):
    
    # unpack file paths:
    MEDIA_DIR = file_paths['MEDIA_DIR']
    dicom_data_file = file_paths['dicom_data']
    segmentation_data_file = file_paths['segmentation_data']
    simpsons_data_file = file_paths['simpsons_data']
    jpeg_destintation = file_paths['dicom_jpegs']
    dicom_webm_destination = file_paths['dicom_webm']
    dicom_mp4_destination = file_paths['dicom_mp4']
    segmentation_mp4_destination = file_paths['segmentation_mp4']
    simpsons_mp4_destination = file_paths['simpsons_mp4']
    
    print('\n[MediaPipeline]__')
    
    # Step 1, get dicom, segmentation data:
    dicom_data = funcs.GetData(dicom_data_file)
    segmentation_data = funcs.GetData(segmentation_data_file)
    simpsons_data = funcs.GetData(simpsons_data_file)
    
    # Step 2, build media base directory:
    funcs.BuildMediaBaseDirectory(MEDIA_DIR)
    
    # Step 3, build videos:
    #funcs.BuildWebm(dicom_data, webm_destination) ## ~15 seconds processing time
    funcs.BuildMP4(dicom_data, dicom_mp4_destination)
    funcs.BuildMP4(segmentation_data, segmentation_mp4_destination)
    funcs.BuildMP4(simpsons_data, simpsons_mp4_destination)