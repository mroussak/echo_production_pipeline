import Tools.ProductionTools as tools
from billiard import Pool
#from multiprocessing import Pool
from decouple import config
from PIL import Image
from time import time
import pandas as pd
import numpy as np
import itertools
import imageio
import ffmpeg
import json
import cv2
import ast
import sys
import os

# Database imports:
sys.path.insert(1, config("BASE_DIR") + 'echo_production_pipeline/Database/EchoData/')
import PostgresCaller



def ParseViewsData(views_data, verbose=False, start=time()):
    
    ''' Accepts views data, returns parsed views data '''

    # intialize data:
    best_views_list = []

    # get list of unique views:
    predicted_views = views_data['predicted_view'].unique()

    # take two best views of each view type:
    for view in predicted_views:
            
        # group by predicted view:
        best_views_object = views_data.loc[views_data['predicted_view'] == view]
        
        # find two best views:
        best_views_object = best_views_object.sort_values(by=['video_view_threshold'], ascending=False)
        best_views_object = best_views_object.iloc[:2]
        
        # append to list:
        best_views_list.append(best_views_object)
            
    # convert to dataframe:
    best_views_data = pd.concat(best_views_list)

    # name dataframe:
    best_views_data.name = view + '_best_views_data'
    
    if verbose:
        print("[@ %7.2f s] [ParseViewsData]: Parsed views_data" %(time()-start))
        
    return best_views_data
    
    
    
def ParseSegmentationApicalData(segmentation_data, verbose=False, start=time()):
    
    ''' Accepts apical segmentation data, returns parsed data '''
    
    for index, row in segmentation_data.iterrows():
    
        # get paths object:
        paths = row['paths']
    
        #  append gif file names to gif file paths:    
        paths['path_to_dicom_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_mask_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_simpsons_gif'] += row['dicom_id'] + '.gif'
    
        # append webm file names to webm file path:
        paths['path_to_dicom_webm'] += row['dicom_id'] + '.webm'
        paths['path_to_mask_webm'] += row['dicom_id'] + '.webm'
        paths['path_to_simpsons_webm'] += row['dicom_id'] + '.webm'
    
        # jpeg root directory:
        paths['path_to_dicom_jpeg_root'] = paths['path_to_dicom_jpeg']
        paths['path_to_mask_jpeg_root'] = paths['path_to_mask_jpeg']
        paths['path_to_simpsons_jpeg_root'] = paths['path_to_simpsons_jpeg']

        # update jpeg paths::
        paths['path_to_dicom_jpeg'] = [paths['path_to_dicom_jpeg'] + file for file in os.listdir(paths['path_to_dicom_jpeg'])]
        paths['path_to_mask_jpeg'] = [paths['path_to_mask_jpeg'] + file for file in os.listdir(paths['path_to_mask_jpeg'])]
        paths['path_to_simpsons_jpeg'] = [paths['path_to_simpsons_jpeg'] + file for file in os.listdir(paths['path_to_simpsons_jpeg'])]

        # replace paths object in dataframe:
        segmentation_data.at[index, 'paths'] = paths
        
    # fill nans with 0s:    
    segmentation_data = segmentation_data.fillna(0)  
    
    segmentation_data.name = 'segmentation_apical_data'

    if verbose:
        print("[@ %7.2f s] [ParseSegmentationApicalData]: Parsed segmentation_data" %(time()-start))
    
    return segmentation_data



def ParseSegmentationPSAXData(segmentation_data, verbose=False, start=time()):
    
    ''' Accepts apical segmentation data, returns parsed data '''
    for index, row in segmentation_data.iterrows():
        
        # get paths object:
        paths = row['paths']
    
        # append gif file names to gif file paths:    
        paths['path_to_dicom_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_mask_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_cylinder_gif'] += row['dicom_id'] + '.gif'
    
        # append webm file names to webm file path:
        paths['path_to_dicom_webm'] += row['dicom_id'] + '.webm'
        paths['path_to_mask_webm'] += row['dicom_id'] + '.webm'
        paths['path_to_cylinder_webm'] += row['dicom_id'] + '.webm'
    
        # jpeg root directories:
        paths['path_to_dicom_jpeg_root'] = paths['path_to_dicom_jpeg']
        paths['path_to_mask_jpeg_root'] = paths['path_to_mask_jpeg']
        paths['path_to_cylinder_jpeg_root'] = paths['path_to_cylinder_jpeg']
        
        # update jpeg paths::
        paths['path_to_dicom_jpeg'] = [paths['path_to_dicom_jpeg'] + file for file in os.listdir(paths['path_to_dicom_jpeg'])]
        paths['path_to_mask_jpeg'] = [paths['path_to_mask_jpeg'] + file for file in os.listdir(paths['path_to_mask_jpeg'])]
        paths['path_to_cylinder_jpeg'] = [paths['path_to_cylinder_jpeg'] + file for file in os.listdir(paths['path_to_cylinder_jpeg'])]
    
        # replace paths object in dataframe:
        segmentation_data.at[index, 'paths'] = paths
    
    # fill nans with 0s:    
    segmentation_data = segmentation_data.fillna(0)    
   
    segmentation_data.name = 'segmentation_psax_data'
    
    if verbose:
        print("[@ %7.2f s] [ParseSegmentationPSAXData]: Parsed segmentation_data" %(time()-start))
    
    return segmentation_data
    


def BuildSingleGif(dicom):

    # build directories to store gifs:
    tools.CreateDirectory(dicom['paths']['path_to_dicom_gif'])
    
    # load video:
    video = tools.LoadVideo(dicom['paths']['path_to_dicom_jpeg'], normalize=False, img_type='jpg', image_dim=None)

    # create gifs:
    imageio.mimsave(dicom['paths']['path_to_dicom_gif'] + dicom['dicom_id'] + '.gif', video)



def BuildGifs(dicom_data, verbose=False, start=time()):
    
    ''' Accepts dicom data, builds gifs '''
        
    NUMBER_OF_THREADS = len(dicom_data)
    
    with Pool(NUMBER_OF_THREADS) as pool:
        
        # create sequence:
        sequence = [dicom_data.iloc[row] for row in range(NUMBER_OF_THREADS)]
        
        # multiprocess:
        total_vidoes = pool.map(BuildSingleGif, sequence)
        
    if verbose:
        print("[@ %7.2f s] [BuildGifs]: Built [%d] gifs" %(time()-start, NUMBER_OF_THREADS))
        
        

def BuildSingleWebm(dicom):
        
        ''' Accepts dicom, builds single webm file '''
        
        try:
            
            # unpack dicom:
            input_files = dicom['input_files']
            output_file = dicom['output_file']
            
            # ffmpeg parameters:
            framerate = 30
            output_options = {
                "format": "webm",
                "pix_fmt": "yuv420p",
                "video_bitrate": 1000000,
                # "-i": os.path.join(clean_dir, '%%01d.jpg')
                # "crf": 10,
            }
      
            # build webm:
            (ffmpeg
                .input(input_files, pattern_type="glob", framerate=framerate)
                .output(output_file, **output_options)
                .global_args('-loglevel', 'quiet', '-y')
                .run()
            )
            
        except Exception as error:
            print('[ERROR] in [build_single_video]: [%s]' %error)



def BuildWebms(dicom_data, verbose=False, start=time()):
    
    ''' Accepts dicom data, builds webms '''
        
    # create list of webms:
    list_of_webms = []
    
    for index, dicom in dicom_data.iterrows():
        
        # general:
        input_files = dicom['paths']['path_to_dicom_jpeg_root'] + '/*.jpg'
        output_file = dicom['paths']['path_to_dicom_webm']
        dicom_webm = {'input_files' : input_files, 'output_file' : output_file}
        list_of_webms.append(dicom_webm)
        
        # a4c, a2c:
        if dicom['predicted_view'] == 'A4C' or dicom['predicted_view'] == 'A2C':
            
            # masks:
            input_files = dicom['paths']['path_to_mask_jpeg_root'] + '/*.jpg'
            output_file = dicom['paths']['path_to_mask_webm']
            mask_webm = {'input_files' : input_files, 'output_file' : output_file}
            list_of_webms.append(mask_webm)
            
            # simpsons:
            input_files = dicom['paths']['path_to_simpsons_jpeg_root'] + '/*.jpg'
            output_file = dicom['paths']['path_to_simpsons_webm']
            simpsons_webm = {'input_files' : input_files, 'output_file' : output_file}
            list_of_webms.append(simpsons_webm)
            
        # psax:
        if dicom['predicted_view'] == 'PSAX':
            
            # masks:
            input_files = dicom['paths']['path_to_mask_jpeg_root'] + '/*.jpg'
            output_file = dicom['paths']['path_to_mask_webm']
            mask_webm = {'input_files' : input_files, 'output_file' : output_file}
            list_of_webms.append(mask_webm)
            
            # cylinder:
            input_files = dicom['paths']['path_to_cylinder_jpeg_root'] + '/*.jpg'
            output_file = dicom['paths']['path_to_cylinder_webm']
            cylinder_webm = {'input_files' : input_files, 'output_file' : output_file}
            list_of_webms.append(cylinder_webm)
        
    # multiprocessing, build each webm file in its own thread:
    NUMBER_OF_THREADS = len(list_of_webms)
    
    with Pool(NUMBER_OF_THREADS) as pool:
        
        # multiprocess:
        total_vidoes = pool.map(BuildSingleWebm, list_of_webms)
        
    if verbose:
        print("[@ %7.2f s] [BuildWebms]: Built [%d] webms" %(time()-start, NUMBER_OF_THREADS))
    


def BuildJsonFromData(data, verbose=False, start=time()):
   
    ''' Accepts data, returns report as json '''
    
    # intialize variables:
    reports_json = []
    
    # get list of unique views:
    unique_views = data['predicted_view'].unique()
    
    # iterate over each view:
    for view in unique_views:
        
        view_data = data.loc[data['predicted_view'] == view]
        #view_data = view_data.sort_values(by='video_view_threshold', ascending=False)
        
        report_object = {
            'view' : view,
            'dicoms' : view_data.to_dict(orient='record'),
        }

        reports_json.append(report_object)
    
    # replace nans:
    reports_json = str(reports_json).replace('nan', '0')
    reports_json = ast.literal_eval(reports_json)
    
    if verbose:
        print("[@ %7.2f s] [BuildJsonFromData]: Built json" %(time()-start))        
    
    return reports_json
    
    
    
def ExportDataToPostgres(reports_json, visit_id, query_file, verbose, start):
    
    ''' Accepts report as json, writes to database '''
    
    # parse json:
    reports_json = str(reports_json)
    reports_json = reports_json.replace("'",'"').replace('None','null').replace('True','true').replace('False','false')
    
    parameters = {
        'visit_id' : int(visit_id),
        'reports_json' : reports_json,
    }
    
    PostgresCaller.main(query_file, parameters)
    
    if verbose:
        print('[@ %7.2f s] [ExportDataToPostgres]: Exported json to postgres to visist with id [%s]' %(time()-start, visit_id))
        