from time import time
import pydicom 
import cv2



def ReadDicomFile(dicom_file_path, verbose=False, start=time()):
    
    ''' Accepts dicom file path, returns dicom
        raises ERROR if file is not a dicom ".dcm" file '''
    
    # # raise error if file is not a dicom file:
    # if dicom_file_path[:-3] != 'dcm':
    #     raise(Exception('[ERROR] in [ReadDicomFile]: iCardio.ai is currently only supporting dicom ".dcm" file formats'))
        
    dicom = pydicom.dcmread(dicom_file_path)
    
    if verbose:
        print('[@ %7.2f s] [ReadDicomFile]: Read dicom from [%s]' %(time()-start, dicom_file_path))
        
    return dicom



def GetManufacturerDetails(dicom, verbose=False, start=time()):
    
    ''' Accepts a dicom object, returns manufacturer detials 
        raises WARNING if manufacturer details cannot be retreived '''
    
    # initialize variables:
    manufacturer_details = {
        'manufacturer' : None,
        'manufacturer_model_name' : None,
    } 
    
    # try accessing data using numeric keys:
    try: 
        manufacturer_details['manufacturer'] = dicom[0x8,0x70].value
        manufacturer_details['manufacturer_model_name'] = dicom[0x8,0x1090].value
    
    except KeyError as error:
        key_error = error
    
    else:
        if verbose:
            print('[@ %7.2f s] [GetManufacturerDetails]: Retreived manufacturer details from dicom' %(time()-start))
        
        return manufacturer_details

    # try accessing data using object attributes:
    try:
        manufacturer_details['manufacturer'] = dicom.Manufacturer 
        manufacturer_details['manufacturer_model_name'] = dicom.ManufacturerModelName
    
    except AttributeError as error:
        attribute_error = error

    else:
        if verbose:
            print('[@ %7.2f s] [GetManufacturerDetails]: Retreived manufacturer details from dicom' %(time()-start))
        
        return manufacturer_details
        
    # print record of warning:
    print('[WARNING] in [GetManufacturerDetails]: Unable to retreive manufacturer details, this may cause issues in future versions')
    print('KeyError: %s' %key_error)
    print('AttributeError: %s' %attribute_error)
        
    if verbose:
        print('[@ %7.2f s] [GetManufacturerDetails]: Unable to retreive manufacturer details from dicom' %(time()-start))
    
    return manufacturer_details
    
    

def GetImageSizeDetails(dicom, verbose=False, start=time()):
    
    ''' Accepts dicom object, returns image size details 
        raises ERROR if image size details cannot be retreived '''
    
    # intialize variables:
    image_size_details = {
        'physical_delta_x' : float('nan'),
        'physical_delta_y' : float('nan'),
        'physical_units_x_direction' : float('nan'),
        'physical_units_y_direction' : float('nan'),
    }
        
    try:
        #image_size_details['physical_units_x_direction'] = dicom[0x18,0x6024].value
        #image_size_details['physical_units_y_direction'] = dicom[0x18,0x6026].value
        image_size_details['physical_delta_x'] = dicom[0x18,0x602c].value
        image_size_details['physical_delta_y'] = dicom[0x18,0x602e].value
        
    except Exception as error:
        raise(Exception('[ERROR] in [GetImageSizeDetails]: Cannot retreive size of image(s) in dicom'))
        print(error)
        
    if verbose:
        print('[@ %7.2f s] [GetImageSizeDetails]: Retreived image size details from dicom' %(time()-start))
    print(image_size_details)
    return image_size_details