import DicomExtractorFunctions as funcs
from time import time



def main(verbose=False, start=time()):
    
    # Variables:
    kwargs = {
        'verbose' : True,
        'start' : start,
        }
    dicom_file_path = 'test'
    dicom_file_path = '/internal_drive/Users/UserID1/Sessions/SessionID1/Dicoms/IM16'
    
    # Step 1, read dicom file:
    dicom = funcs.ReadDicomFile(dicom_file_path, **kwargs)
    
    # Step 2, get manufacturer details:
    manufacturer_details = funcs.GetManufacturerDetails(dicom, **kwargs)
    
    # Step 3, get image size details:
    image_size_details =  funcs.GetImageSizeDetails(dicom, **kwargs)

if __name__ == '__main__':
    
    main()