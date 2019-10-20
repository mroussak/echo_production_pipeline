import Tools.ProductionTools as tools
from multiprocessing import Pool
from PIL import Image
from time import time
import pandas as pd
import numpy as np
import pydicom 
import imageio
import hashlib
import sys
import cv2
import os

# Preprocessor imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/Preprocessor/')
import Preprocessor



def ReadDicoms(dicoms_directory, verbose=False, start=time()):

    ''' Accepts patient directory, returns list of pydicoms '''
    
    # initialize variables:
    dicoms_file_list = os.listdir(dicoms_directory)
    
    NUMBER_OF_THREADS = len(dicoms_file_list)
    
    with Pool(NUMBER_OF_THREADS) as pool:
        dicoms = pool.map(Preprocessor.main, [dicoms_directory + file for file in dicoms_file_list])
        pool.close()

    if verbose:
        print("[@ %7.2f s] [ReadDicoms]: Read [%d] dicoms from [%s]" %(time()-start, len(dicoms), dicoms_directory))
    
    return dicoms



def parse_single_dicom(counter, dicom, videos_directory):

    # create dicom_id:
    #dicom_id = counter
    unique_identifier = dicom['status']['dicom_file_path'].encode('utf-8')
    dicom_id = hashlib.sha256(unique_identifier).hexdigest()[:6]
    
    # name new directories:
    path_to_dicom_jpeg = '%s%s/Jpeg/' % (videos_directory, dicom_id)
    path_to_dicom_gif = '%s%s/Gif/' % (videos_directory, dicom_id)

    # build dicom_object
    dicom_object = {
        'dicom_id': dicom_id,
        'dicom_type': dicom['dicom']['dicom_type'],
        'usable' : dicom['status']['status_code'] != 2,
        'paths': {
            'path_to_dicom_jpeg': path_to_dicom_jpeg,
            'path_to_dicom_gif': path_to_dicom_gif,
        },
        'config': {
            'manufacturer' : dicom['dicom']['manufacturer'],
            'manufacturer_model_name' : dicom['dicom']['manufacturer_model_name'],
            'number_of_frames': dicom['dicom']['number_of_frames'],
            'frame_time': None,
            'x_scale': dicom['dicom']['physical_units_x_direction'],
            'y_scale': dicom['dicom']['physical_units_y_direction'],
            'len_x_pix': dicom['dicom']['physical_delta_x'],
            'len_y_pix': dicom['dicom']['physical_delta_y'],
        },
    }

    # build pixel_array_object:
    pixel_array_object = {
        'dicom_id': dicom_id,
        'pixel_array': dicom['dicom']['pixel_data'],
        'path_to_dicom_jpeg': path_to_dicom_jpeg,
    }

    # return an empty object if dicom is unusable
    if dicom_object['usable'] == False:
        return None

    return dicom_object, pixel_array_object


    
def ParseDicoms(dicoms, videos_directory, verbose=False, start=time()):
    
    ''' Accepts list of dicoms, returns dataframe of dicoms '''

    # iterate over each dicom:
    dicom_info = []
    
    for counter, dicom in enumerate(dicoms):
        dicom_info.append((counter,dicom,videos_directory))

    NUMBER_OF_THREADS = len(dicoms)

    with Pool(NUMBER_OF_THREADS) as pool:
        multi_proc_output = pool.starmap(parse_single_dicom, dicom_info)
        pool.close()

    multi_proc_output = list(filter(None,multi_proc_output))

    try:
        dicom_data, pixel_array_data = zip(*multi_proc_output)

    except ValueError as error:
        raise(ValueError('[ERROR] in [ParseDicomData]: No usable views found, currently only using standard views, V:[%s]' %error))

    # convert list data to dataframe:
    dicom_data = pd.DataFrame(dicom_data)
    dicom_data.name = 'dicom_data'
    # pixel_array_data = pd.DataFrame(pixel_array_data)
    # pixel_array_data.name = 'pixel_array_data'

    if verbose:
        print("[@ %7.2f s] [ParseDicoms]: Parsed [%d] dicoms" %(time()-start, len(dicom_data)))    
    
    return dicom_data, pixel_array_data



def AnonymizeDicoms(pixel_array_data, verbose=False, start=time()):

    ''' Accepts dicoms as pixel array data, returns anonymized dicoms as pixel array data '''
    
    if verbose:
        print("[@ %7.2f s] [AnonymizeDicoms]: Anonymized dicoms" %(time()-start))  
        
    return pixel_array_data



def build_single_video(dicom):
    
    # build directories to store videos:
    tools.CreateDirectory(dicom['path_to_dicom_jpeg'])

    # check number of frames:
    if len(dicom['pixel_array'].shape) == 3:
        number_of_frames = 1
    elif len(dicom['pixel_array'].shape) == 4:
        number_of_frames = dicom['pixel_array'].shape[0]

    # only one frame in dicom:
    if number_of_frames == 1:

        # name new image:
        image_name = '%s%d.jpg' % (dicom['path_to_dicom_jpeg'], 0)

        # build jpeg file from dicom data:
        image = cv2.cvtColor(dicom['pixel_array'], cv2.COLOR_RGB2GRAY)
        image = Image.fromarray(image)

        # save image:
        image.save(image_name)

    # multiple frames in dicom:
    else:

        # convert each frame to jpeg:
        for counter2, frame in enumerate(dicom['pixel_array']):
            
            # name new image:
            image_name = '%s%d.jpg' % (dicom['path_to_dicom_jpeg'], counter2)

            # build jpeg file from dicom data:
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            image = Image.fromarray(image)

            # save image:
            image.save(image_name)



def BuildVideos(pixel_array_data, verbose=False, start=time()):
    
    ''' Accepts dicom_data dataframe, builds folder with jpeg file of each frame '''

    NUMBER_OF_THREADS = len(pixel_array_data)

    with Pool(NUMBER_OF_THREADS) as pool:
        pool.map(build_single_video, pixel_array_data)
            
    if verbose:
        print("[@ %7.2f s] [BuildVideos]: Built [%d] videos" %(time()-start, len(pixel_array_data)))



