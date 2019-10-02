import cv2
import json
import itertools
import numpy as np
import pandas as pd
from PIL import Image
from time import time
import Tools.ProductionTools as tools



def ParseSegmentationApicalData(segmentation_data, verbose=False, start=time()):
    
    ''' Accepts apical segmentation data, returns parsed data '''
    
    # append gif file names to gif file paths:
    segmentation_data['path_to_dicom_gif'] = segmentation_data['path_to_dicom_gif'].map(str) + segmentation_data['dicom_id'].map(str) + '.gif'
    segmentation_data['path_to_mask_gif'] = segmentation_data['path_to_mask_gif'].map(str) + segmentation_data['dicom_id'].map(str) + '.gif'
    segmentation_data['path_to_simpsons_gif'] = segmentation_data['path_to_simpsons_gif'].map(str) + segmentation_data['dicom_id'].map(str) + '.gif'
    
    # build file path list to jpegs:
    for index, dicom in segmentation_data.iterrows(): 
        
        dicom_jpegs = []
        mask_jpegs = []
        simpsons_jpegs = []
        
        for i in range(dicom['number_of_frames']):
    
            dicom_jpegs.append(dicom['path_to_dicom_jpeg'] + str(i) + '.jpg')
            mask_jpegs.append(dicom['path_to_mask_jpeg'] + str(i) + '.jpg')
            simpsons_jpegs.append(dicom['path_to_simpsons_jpeg'] + str(i) + '.jpg')
    
        # add jpeg list to dataframe:
        segmentation_data.at[index, 'path_to_dicom_jpeg'] = dicom_jpegs
        segmentation_data.at[index, 'path_to_mask_jpeg'] = mask_jpegs
        segmentation_data.at[index, 'path_to_simpsons_jpeg'] = simpsons_jpegs

    # convert np arrays to list
    segmentation_data['lvv_simpson'] = segmentation_data['lvv_simpson'].apply(lambda x: np.nan_to_num(x))
    segmentation_data['lvv_simpson'] = segmentation_data['lvv_simpson'].apply(lambda x: list(x))
    segmentation_data = segmentation_data.fillna(0)
        
    if verbose:
        print("[@ %7.2f s] [ParseSegmentationApicalData]: Parsed segmentation_data" %(time()-start))
    
    return segmentation_data
    


def ResizeVideos(segmentation_apical_data, verbose=False, start=time()):
    
    ''' Accepts data, rewrites videos with less pixels '''
    
    # get jpeg files:
    dicom_jpegs = list(segmentation_apical_data['path_to_dicom_jpeg'])
    mask_jpegs = list(segmentation_apical_data['path_to_mask_jpeg'])
    simpsons_jpegs = list(segmentation_apical_data['path_to_simpsons_jpeg'])
    jpeg_files = dicom_jpegs + mask_jpegs + simpsons_jpegs
    jpeg_files = itertools.chain(*jpeg_files)
    
    print(jpeg_files)
    
    # resize each image:
    for filepath in jpeg_files:
        image = cv2.imread(filepath)
        image = cv2.resize(image, None, fx=0.5, fy=0.5)
        new_image = Image.fromarray(image)
        new_image.save(filepath) 
    
    if verbose:
        print("[@ %7.2f s] [ResizeVideos]: Resized videos" %(time()-start))
    


def BuildJsonFromData(data, verbose=False, start=time()):
    
    ''' Accepts data, returns report as json '''
    
    # intialize variables:
    reports_json = []
    
    # get list of unique views:
    unique_views = data['predicted_view'].unique()
    
    # iterate over each view:
    for view in unique_views:
        
        view_data = data.loc[data['predicted_view'] == view]
        view_data = view_data.sort_values(by='video_view_threshold', ascending=False)
        
        report_object = {
            'view' : view,
            'dicoms' : view_data.to_dict(orient='record'),
        }
        
        reports_json.append(report_object)
    
    if verbose:
        print("[@ %7.2f s] [BuildJsonFromData]: Built json" %(time()-start))        
    
    return reports_json
    
    
    