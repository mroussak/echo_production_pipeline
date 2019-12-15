from time import time
import numpy as np
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
            print('[@ %7.2f s] [GetManufacturerDetails]: Retreived manufacturer details from dicom using numeric keys' %(time()-start))
        
        return manufacturer_details

    # try accessing data using object attributes:
    try:
        manufacturer_details['manufacturer'] = dicom.Manufacturer 
        manufacturer_details['manufacturer_model_name'] = dicom.ManufacturerModelName
    
    except AttributeError as error:
        attribute_error = error

    else:
        if verbose:
            print('[@ %7.2f s] [GetManufacturerDetails]: Retreived manufacturer details from dicom using object attributes' %(time()-start))
        
        return manufacturer_details
        
    if verbose:
        print('[WARNING] in [GetManufacturerDetails]: Unable to retreive manufacturer details, this may cause issues in future versions K:[%s] A:[%s]' %(key_error, attribute_error))
    
    return manufacturer_details
    
    

def GetImageSizeDetails(dicom, verbose=False, start=time()):
    
    ''' Accepts dicom object, returns image size details 
        raises ERROR if image size details cannot be retreived '''
    
    # intialize variables:
    image_size_details = {
        'physical_delta_x' : None,
        'physical_delta_y' : None,
        'physical_units_x_direction' : None,
        'physical_units_y_direction' : None,
    }
    
    ''' Extraction method for:
        'Sonoscanner', '''
    
    # try accessing data using numeric keys:
    try: 
        image_size_details['physical_units_x_direction'] = dicom[0x18,0x6024].value
        image_size_details['physical_units_y_direction'] = dicom[0x18,0x6026].value
        image_size_details['physical_delta_x'] = abs(dicom[0x18,0x602c].value)
        image_size_details['physical_delta_y'] = abs(dicom[0x18,0x602e].value)
    
    except KeyError as error:
        key_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetImageSizeDetails]: Retreived image size details from dicom using numeric keys' %(time()-start))
            
        return image_size_details

    # try accessing data using object attributes:
    try:
	    image_size_details['physical_units_x_direction'] = dicom.PhysicalUnitsXDirection
	    image_size_details['physical_units_y_direction'] = dicom.PhysicalUnitsYDirection
	    image_size_details['physical_delta_x'] = abs(dicom.PhysicalDeltaX)
	    image_size_details['physical_delta_y'] = abs(dicom.PhysicalDeltaY)
        
    except AttributeError as error:
        attribute_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetImageSizeDetails]: Retreived image size details from dicom using object attributes' %(time()-start))
            
        return image_size_details  
        
    ''' Extraction method for:
        'Acuson Cypress', 'GE Healthcare LOGIQe',
        'GE Healthcare Ultrasound Vivid iq', 'GE Healthcare Vivid i',
        'GE Healthcare Vivide', 'GEMS Ultrasound Vivid i', 'MINDRAY M7', 'SIEMENS ACUSON P500',
        'Teratech Corp. Terason Ultrasound Imaging System' '''
    
    # try accessing data using numeric keys:
    try: 
        image_size_details['physical_units_x_direction'] = dicom[0x18,0x6011][0][0x18,0x6024].value
        image_size_details['physical_units_y_direction'] = dicom[0x18,0x6011][0][0x18,0x6026].value
        image_size_details['physical_delta_x'] = abs(dicom[0x18,0x6011][0][0x18,0x602c].value)
        image_size_details['physical_delta_y'] = abs(dicom[0x18,0x6011][0][0x18,0x602e].value)

    except KeyError as error:
        key_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetImageSizeDetails]: Retreived image size details from dicom using numeric keys' %(time()-start))
            
        return image_size_details
    
    # try accessing data using object attributes:
    try: 
        image_size_details['physical_units_x_direction'] = dicom.SequenceOfUltrasoundRegions[0].PhysicalUnitsXDirection
        image_size_details['physical_units_y_direction'] = dicom.SequenceOfUltrasoundRegions[0].PhysicalUnitsYDirection
        image_size_details['physical_delta_x'] = abs(dicom.SequenceOfUltrasoundRegions[0].PhysicalDeltaX)
        image_size_details['physical_delta_y'] = abs(dicom.SequenceOfUltrasoundRegions[0].PhysicalDeltaY)
        
    except AttributeError as error:
        attribute_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetImageSizeDetails]: Retreived image size details from dicom using object attributes' %(time()-start))
            
        return image_size_details
        
    if verbose:
        print(Exception('[ERROR] in [GetImageSizeDetails]: Unable to retreive image size details from dicom K:[%s] A:[%s]' %(key_error, attribute_error)))
    
    return image_size_details
    
    

def GetDicomTypeDetails(dicom, verbose=False, start=time()):
    
    ''' Accepts dicom object, returns dicom type '''
    
    # initilaize varibles:
    dicom_type_details = None
    
    ''' Extraction method for:
        'Sonoscanner', '''
    
    # try accessing data using numeric keys:
    try: 
        if (dicom[0x18, 0x6014].value == 1) or (dicom[0x18, 0x6014].value == 0) :
            dicom_type_details = 'standard'
        elif dicom[0x18, 0x6014].value == 2:
            dicom_type_details = 'color'
        else:
            print(Exception('[ERROR] in [GetDicomTypeDetails]: Cannot determine dicom type'))
            return dicom_type_details 

    except KeyError as error:
        key_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetDicomTypeDetails]: Retreived dicom type details from dicom using numeric keys' %(time()-start))
            
        return dicom_type_details
            
    # try accessing data using object attributes:
    try: 
        if (dicom.RegionDataType == 1) or (dicom.RegionDataType == 0):
            dicom_type_details = 'standard'
        elif dicom.RegionDataType == 2:
            dicom_type_details = 'color'
        else:
            print(Exception('[ERROR] in [GetDicomTypeDetails]: Cannot determine dicom type'))
            return dicom_type_details
        
    except AttributeError as error:
        attribute_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetDicomTypeDetails]: Retreived dicom type details from dicom using object attributes' %(time()-start))
            
        return dicom_type_details
            
    
    ''' Extraction method for:
        'Acuson Cypress', 'GE Healthcare LOGIQe',
        'GE Healthcare Ultrasound Vivid iq', 'GE Healthcare Vivid i',
        'GE Healthcare Vivide', 'GEMS Ultrasound Vivid i', 'MINDRAY M7', 'SIEMENS ACUSON P500',
        'Teratech Corp. Terason Ultrasound Imaging System' '''
    
    # check if dicom is neither standard nor color:
    if pydicom.tag.Tag((0x18,0x6011)) not in dicom.keys():
        print(Exception('[ERROR] in [GetDicomTypeDetails]: Cannot determine dicom type'))
        return dicom_type_details
    
    # try accessing data using numeric keys:
    try: 
        if dicom[0x18, 0x6011][0][0x18, 0x6014].value == 1:
            dicom_type_details = 'standard'
        elif dicom[0x18, 0x6011][0][0x18, 0x6014].value == 2:
            dicom_type_details = 'color'
        else:
            print(Exception('[ERROR] in [GetDicomTypeDetails]: Cannot determine dicom type'))
            return dicom_type_details

    except KeyError as error:
        key_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetDicomTypeDetails]: Retreived dicom type details from dicom using numeric keys' %(time()-start))
            
        return dicom_type_details
    
    # try accessing data using object attributes:
    try: 
        if dicom.SequenceOfUltrasoundRegions[0].RegionDataType == 1:
            dicom_type_details = 'standard'
        elif dicom.SequenceOfUltrasoundRegions[0].RegionDataType == 2:
            dicom_type_details = 'color'
        else:
            print(Exception('[ERROR] in [GetDicomTypeDetails]: Cannot determine dicom type'))
            return dicom_type_details
        
    except AttributeError as error:
        attribute_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetDicomTypeDetails]: Retreived dicom type details from dicom using object attributes' %(time()-start))
            
        return dicom_type_details
    
    if verbose:   
        print(Exception('[ERROR] in [GetDicomTypeDetails]: Unable to retreive dicom type from dicom K:[%s] A:[%s]' %(key_error, attribute_error)))
    
    return dicom_type_details
    
    

def GetNumberOfFramesDetails(dicom, verbose=False, start=time()):
    
    ''' Accepts dicom object, returns number of frames in dicom '''
    
    # initialize variables:
    number_of_frames_details = None
    
    # try accessing data using numeric keys:
    try: 
        number_of_frames_details = dicom[0x28,0x8].value

    except KeyError as error:
        key_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetNumberOfFramesDetails]: Retreived number of frames from dicom using numeric keys' %(time()-start))
            
        return number_of_frames_details
    
    # try accessing data using object attributes:
    try: 
       number_of_frames_details = dicom.NumberOfFrames
        
    except AttributeError as error:
        attribute_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetNumberOfFramesDetails]: Retreived number of frames from dicom using object attributes' %(time()-start))
            
        return number_of_frames_details
        
    if verbose:
       print(Exception('[ERROR] in [GetNumberOfFramesDetails]: Unable to retreive number of frames from dicom K:[%s] A:[%s]' %(key_error, attribute_error)))
    
    return number_of_frames_details
    


def GetPixelArrayDataDetails(dicom, verbose=False, start=time()):
    
    ''' Accepts dicom object, returns pixel array data details '''
    
    # intialize variables:
    pixel_array_data_details = None
    
    # try accessing data using numeric keys:
    try: 
        pixel_array_data_details = dicom.pixel_array

    except (AttributeError, ValueError) as error:
        attribute_or_value_error = error
        
    else:
        if verbose:
            print('[@ %7.2f s] [GetPixelArrayDataDetails]: Retreived pixel array from dicom using pydicom method .pixel_array' %(time()-start))
            
        return pixel_array_data_details
    
  
    if verbose:
       print(Exception('[ERROR] in [GetPixelArrayDataDetails]: Unable to retreive pixel data from dicom A/V:[%s]' %(attribute_or_value_error)))
    
    return pixel_array_data_details
    
    

def CompileDicomDetails(manufacturer_details, image_size_details, dicom_type_details, number_of_frames_details, pixel_data_details, verbose=False, start=time()):
    
    ''' Accepts dicom details, returns compiled dicom object '''
    
    dicom = {
        'manufacturer' : manufacturer_details['manufacturer'],
        'manufacturer_model_name' : manufacturer_details['manufacturer_model_name'],
        'physical_units_x_direction' : image_size_details['physical_units_x_direction'],
        'physical_units_y_direction' : image_size_details['physical_units_y_direction'],
        'physical_delta_x' : image_size_details['physical_delta_x'],
        'physical_delta_y' : image_size_details['physical_delta_y'],
        'dicom_type' : dicom_type_details,
        'number_of_frames' : number_of_frames_details,
        'pixel_data' : pixel_data_details,
    }
    
    if verbose:
        print('[@ %7.2f s] [CompileDicomDetails]: Compiled dicom' %(time()-start))
    
    return dicom
    
    