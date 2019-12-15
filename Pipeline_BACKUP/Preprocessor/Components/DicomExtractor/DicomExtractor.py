import Components.DicomExtractor.DicomExtractorFunctions as funcs
from time import time



def main(dicom_file_path, verbose=False, start=time()):
    
    # Variables:
    kwargs = {
        'verbose' : verbose,
        'start' : start,
    }

    # Step 1, read dicom file:
    dicom = funcs.ReadDicomFile(dicom_file_path, **kwargs)
    
    # Step 2, get manufacturer details:
    manufacturer_details = funcs.GetManufacturerDetails(dicom, **kwargs)
    
    # Step 3, get image size details:
    image_size_details =  funcs.GetImageSizeDetails(dicom, **kwargs)
    
    # Step 4, get dicom type:
    dicom_type_details = funcs.GetDicomTypeDetails(dicom, **kwargs)

    # Step 5, get number of frames:
    number_of_frames_details = funcs.GetNumberOfFramesDetails(dicom, **kwargs)

    # Step 6, get pixel data:
    pixel_data_details = funcs.GetPixelArrayDataDetails(dicom, **kwargs)

    # Step 7, compile dicom details:
    dicom = funcs.CompileDicomDetails(manufacturer_details, image_size_details, dicom_type_details, number_of_frames_details, pixel_data_details, **kwargs)
    
    # Step 8, export dicom:
    return dicom


        