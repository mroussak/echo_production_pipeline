import os
import cv2
import pydicom 
import imageio
import numpy as np
import pandas as pd
from time import time
from PIL import Image
import Tools.ProductionTools as tools



def ReadDicoms(dicoms_directory, verbose=False, start=time()):
    
    ''' Accepts patient directory, returns list of pydicoms '''
    
    # initialize variables:
    dicoms = []
    dicoms_file_list = os.listdir(dicoms_directory)
    
    # get list of dicoms:
    for file in dicoms_file_list:
        dicom = pydicom.dcmread(dicoms_directory + file)  
        dicoms.append(dicom)
    
    if verbose:
        print("[@ %7.2f s] [ReadDicoms]: Read dicoms from [%s]" %(time()-start, dicoms_directory))
    
    return dicoms
    
    
    
def ParseDicoms(dicoms, videos_directory, verbose=False, start=time()):
    
    ''' Accepts list of dicoms, returns dataframe of dicoms '''
    
    # intialize empty dataframes:
    dicom_data = []
    pixel_array_data = []
        
    # iterate over each dicom:
    for counter, dicom in enumerate(dicoms):
        
        try:
        
            # create dicom id:
            dicom_id = '%s_%02d' %(dicom.PatientID, counter)

            # check number of frames:
            if len(dicom.pixel_array.shape) == 3:
                number_of_frames = 1
                frame_time = float('nan')
                dicom_type = 'single'

            elif len(dicom.pixel_array.shape) == 4:
                number_of_frames = dicom.pixel_array.shape[0]
                
                try:
                    frame_time = dicom[0x18,0x1063].value 
                except:
                    frame_time = np.nan 

                # check dicom type:
                if len(list(dicom[0x18,0x6011])) == 1:

                    # check if the type is a color image:
                    if dicom[0x18,0x6011][0][0x18,0x6014].value == 2:
                        dicom_type = 'color'
                    else:
                        dicom_type = 'standard'                       

            # name new directories:
            path_to_dicom_jpeg = '%s%s/Jpeg/' %(videos_directory, dicom_id)
            path_to_dicom_gif = '%s%s/Gif/' %(videos_directory, dicom_id)

            # build dicom_object    
            dicom_object = {
                'dicom_id' : dicom_id,
                'patient_id' : dicom.PatientID,
                'path_to_dicom_jpeg' : path_to_dicom_jpeg,
                'path_to_dicom_gif' : path_to_dicom_gif,
                'dicom_type' : dicom_type,
                'number_of_frames' : number_of_frames,
                'frame_time' : frame_time, 
                'x_scale' : dicom[0x18,0x6011][0][0x18,0x6024].value, 
                'y_scale' : dicom[0x18,0x6011][0][0x18,0x6026].value,
                'len_x_pix' : abs(dicom[0x18,0x6011][0][0x18,0x602c].value),
                'len_y_pix' : abs(dicom[0x18,0x6011][0][0x18,0x602e].value),
            }

            # build pixel_array_object:
            pixel_array_object = {
                'dicom_id' : str(dicom.PatientID) + '_' + str(counter), 
                'pixel_array' : dicom.pixel_array,
                'path_to_dicom_jpeg' : path_to_dicom_jpeg,
            }

            # append objects to data lists:
            dicom_data.append(dicom_object)
            pixel_array_data.append(pixel_array_object)
        
        except Exception as e:
            pass
        
    # converrt list data to dataframe:    
    dicom_data = pd.DataFrame(dicom_data)
    dicom_data.name = 'dicom_data'
    pixel_array_data = pd.DataFrame(pixel_array_data)
    pixel_array_data.name = 'pixel_array_data'
    
    if verbose:
        print("[@ %7.2f s] [ParseDicoms]: Parsed [%d] dicoms" %(time()-start, len(dicom_data)))    
    
    return dicom_data, pixel_array_data



def BuildVideos(pixel_array_data, verbose=False, start=time()):
    
    ''' Accepts dicom_data dataframe, builds folder with jpeg file of each frame '''
    
    for index, dicom in pixel_array_data.iterrows():
    
        # build directories to store videos:
        tools.CreateDirectory(dicom["path_to_dicom_jpeg"])
        
        # check number of frames:
        if len(dicom.pixel_array.shape) == 3:
            number_of_frames = 1
        elif len(dicom.pixel_array.shape) == 4:
            number_of_frames = dicom.pixel_array.shape[0]
        
        # only one frame in dicom:
        if number_of_frames == 1:
            
            # name new image:
            image_name = '%s%d.jpg' %(dicom['path_to_dicom_jpeg'], 0)

            # build jpeg file from dicom data:
            image = cv2.cvtColor(dicom.pixel_array, cv2.COLOR_RGB2GRAY)
            image = Image.fromarray(image)

            # save image:
            image.save(image_name)   
                            
        # multiple frames in dicom:
        else:
        
            # convert each frame to jpeg:
            for counter2, frame in enumerate(dicom.pixel_array):

                # name new image:
                image_name = '%s%d.jpg' %(dicom['path_to_dicom_jpeg'], counter2)

                # build jpeg file from dicom data:
                image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                image = Image.fromarray(image)

                # save image:
                image.save(image_name)     
            
    if verbose:
        print("[@ %7.2f s] [BuildVideos]: Built [%d] videos" %(time()-start, len(pixel_array_data)))
    

    
def BuildGifs(dicom_data, verbose=False, start=time()):
    
    ''' Accepts dicom data, build gifs '''
    
    for index, dicom in dicom_data.iterrows():
        
        # build directories to store gifs:
        tools.CreateDirectory(dicom["path_to_dicom_gif"])
        
        try:
            video = tools.LoadVideo(dicom['path_to_dicom_jpeg'], normalize=False, img_type='jpg', image_dim=None)
            imageio.mimsave(dicom['path_to_dicom_gif'] + dicom['dicom_id'] + ".gif", video)
        except Exception as exception:
            print(exception)
            pass

    if verbose:
        print("[@ %7.2f s] [BuildGifs]: Built [%d] gifs" %(time()-start, len(dicom_data)))