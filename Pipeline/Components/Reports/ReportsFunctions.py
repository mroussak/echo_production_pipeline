import cv2
import ast
import json
import itertools
import numpy as np
import pandas as pd
from PIL import Image
from time import time
import Tools.ProductionTools as tools



def ParseSegmentationApicalData(segmentation_data, verbose=False, start=time()):
    
    ''' Accepts apical segmentation data, returns parsed data '''
    
    for index, row in segmentation_data.iterrows():
    
        # get paths object:
        paths = row['paths']
    
        #  append gif file names to gif file paths:    
        paths['path_to_dicom_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_mask_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_simpsons_gif'] += row['dicom_id'] + '.gif'
            
        # build file path list to jpegs:
        dicom_jpegs = []
        mask_jpegs = []
        simpsons_jpegs = []
        
        for i in range(row['config']['number_of_frames']):
    
            dicom_jpegs.append(paths['path_to_dicom_jpeg'] + str(i) + '.jpg')
            mask_jpegs.append(paths['path_to_mask_jpeg'] + str(i) + '.jpg')
            simpsons_jpegs.append(paths['path_to_simpsons_jpeg'] + str(i) + '.jpg')
    
        # update paths object:
        paths['path_to_dicom_jpeg'] = dicom_jpegs
        paths['path_to_mask_jpeg'] = mask_jpegs
        paths['path_to_simpsons_jpeg'] = simpsons_jpegs
    
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
    
        #  append gif file names to gif file paths:    
        paths['path_to_dicom_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_mask_gif'] += row['dicom_id'] + '.gif'
        paths['path_to_cylinder_gif'] += row['dicom_id'] + '.gif'
            
        # build file path list to jpegs:
        dicom_jpegs = []
        mask_jpegs = []
        cylinder_jpegs = []
        
        for i in range(row['config']['number_of_frames']):
    
            dicom_jpegs.append(paths['path_to_dicom_jpeg'] + str(i) + '.jpg')
            mask_jpegs.append(paths['path_to_mask_jpeg'] + str(i) + '.jpg')
            cylinder_jpegs.append(paths['path_to_cylinder_jpeg'] + str(i) + '.jpg')
    
        # update paths object:
        paths['path_to_dicom_jpeg'] = dicom_jpegs
        paths['path_to_mask_jpeg'] = mask_jpegs
        paths['path_to_cylinder_jpeg'] = cylinder_jpegs
    
        # replace paths object in dataframe:
        segmentation_data.at[index, 'paths'] = paths
    
    # fill nans with 0s:    
    segmentation_data = segmentation_data.fillna(0)    
    
    segmentation_data.name = 'segmentation_psax_data'
    
    if verbose:
        print("[@ %7.2f s] [ParseSegmentationPSAXData]: Parsed segmentation_data" %(time()-start))
    
    return segmentation_data
    


def ResizeVideos(data, verbose=False, start=time()):
    
    ''' Accepts data, rewrites videos with less pixels '''
    
    # for index, row in data.iterrows():
    
    #     # get jpeg files:
    #     dicom_jpegs = list(row['paths']['path_to_dicom_jpeg'])
    #     mask_jpegs = list(row['paths']['path_to_mask_jpeg'])
        
    #     if row['predicted_view'] == 'PSAX':
    #         other_jpegs = list(row['paths']['path_to_cylinder_jpeg'])
    #     else:
    #         other_jpegs = list(row['paths']['path_to_simpsons_jpeg'])
        
    #     jpeg_files = dicom_jpegs + mask_jpegs + other_jpegs
        
    #     # resize each image:
    #     try:
    #         for filepath in jpeg_files:
    #             image = cv2.imread(filepath)
    #             image = cv2.resize(image, None, fx=0.5, fy=0.5)
    #             new_image = Image.fromarray(image)
    #             new_image.save(filepath) 
    #     except:
    #         pass
        
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
    
    
    