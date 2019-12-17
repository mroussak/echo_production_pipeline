from  Pipeline.Components.Dicoms import DicomsFunctions as funcs
from  Pipeline.Configuration.Configuration import configuration
from  Pipeline.Tools import Tools as tools



def DicomsPipeline(file_paths):
    
    # unpack files:
    dicom_id = file_paths['dicom_id']
    destination_directory = file_paths['DICOMS_DIR']
    dicom_data_destination = file_paths['dicom_data']
    
    print('\n[DicomExtractorPipeline]__')
    
    # Step 1, download file from s3:
    dicom_file_path = funcs.DownloadFileFromS3(dicom_id, destination_directory)
    
    # Step 2, read dicom file:
    dicom = funcs.ReadDicomFile(dicom_file_path)
    
    # Step 3, get manufacturer details:
    manufacturer_details = funcs.GetManufacturerDetails(dicom)
    
    # Step 4, get image size details:
    image_size_details =  funcs.GetImageSizeDetails(dicom)
    
    # Step 5, get dicom type:
    dicom_type_details = funcs.GetDicomTypeDetails(dicom)

    # Step 6, get number of frames:
    number_of_frames_details = funcs.GetNumberOfFramesDetails(dicom)

    # Step 7, get pixel data:
    pixel_data_details = funcs.GetPixelArrayDataDetails(dicom)

    # Step 8, compile dicom details:
    dicom = funcs.CompileDicomDetails(dicom_id, manufacturer_details, image_size_details, dicom_type_details, number_of_frames_details, pixel_data_details)
    
    # Step 9, export dicom:
    funcs.ExportDicom(dicom, dicom_data_destination)