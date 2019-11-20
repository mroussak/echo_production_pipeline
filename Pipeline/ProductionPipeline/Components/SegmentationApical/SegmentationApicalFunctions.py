import Components.Models.ModelsPipeline as models
import Tools.ProductionTools as tools
from billiard import Pool
#from multiprocessing import Pool
from time import time
import pandas as pd
import numpy as np
import importlib
import yaml
import os



def ParseViewsData(views_data, view, videos_directory, verbose=False, start=time()):
    
    ''' Accepts views data, returns parsed views data '''

    # sort for relevant data:
    views_data = views_data.loc[views_data['predicted_view'] == view]
    
    # take two best views:
    views_data = views_data.sort_values(by=['video_view_threshold'], ascending=False)
    views_data = views_data.iloc[:2]

    for index, row in views_data.iterrows():
        
        # build new directories:
        paths = {
            'path_to_dicom_jpeg' : row['paths']['path_to_dicom_jpeg'],
            'path_to_dicom_gif' : row['paths']['path_to_dicom_gif'],
            'path_to_dicom_webm' : row['paths']['path_to_dicom_webm'],
            'path_to_mask_jpeg' : videos_directory + 'SegmentationApical/SegmentationMasks/' + row['dicom_id'] + '/Jpeg/',
            'path_to_mask_gif' : videos_directory + 'SegmentationApical/SegmentationMasks/' + row['dicom_id'] + '/Gif/',
            'path_to_mask_webm' : videos_directory + 'SegmentationApical/SegmentationMasks/' + row['dicom_id'] + '/Webm/',
            'path_to_simpsons_jpeg' : videos_directory + 'SegmentationApical/SimpsonsMethod/' + row['dicom_id'] + '/Jpeg/',
            'path_to_simpsons_gif' : videos_directory + 'SegmentationApical/SimpsonsMethod/' + row['dicom_id'] + '/Gif/',
            'path_to_simpsons_webm' : videos_directory + 'SegmentationApical/SimpsonsMethod/' + row['dicom_id'] + '/Webm/',
        }
    
        views_data.at[index, 'paths'] = paths

    # name dataframe:
    views_data.name = view + '_views_data'
    
    if verbose:
        print("[@ %7.2f s] [ParseViewsData]: Parsed views_data" %(time()-start))
        
    return views_data



def PredictSegmentation(views_data, model, verbose=False, start=time()):
    
    ''' Accepts views data, segmentation model, returns predictions '''
    
    # initialize variables:
    masks = []

    # predict on each frame:
    for index, dicom in views_data.iterrows():
        
        try:
            # load videos:
            frames = tools.LoadVideo(dicom['paths']['path_to_dicom_jpeg'], img_type='jpg', normalize='frame')
            frames = frames.reshape(frames.shape + (1,))

            # predict view:
            if model == 'A4C':
                with models.graph.as_default():
                    prediction = models.a4c_segmentation_model.predict(frames, verbose=0)

            if model =='A2C':
                with models.graph.as_default():
                    prediction = models.a2c_segmentation_model.predict(frames, verbose=0)

            # create mask object:
            mask = {
                'mask' : prediction,
                'dicom_id' : dicom['dicom_id'],
                'len_x_pix' : dicom['config']['len_x_pix'],
                'len_y_pix' : dicom['config']['len_y_pix'],
                'path_to_dicom_jpeg' : dicom['paths']['path_to_dicom_jpeg'],
                'path_to_mask_jpeg' : dicom['paths']['path_to_mask_jpeg'],
                'path_to_mask_gif' : dicom['paths']['path_to_mask_gif'],
                'path_to_mask_webm' : dicom['paths']['path_to_mask_webm'],
                'path_to_simpsons_jpeg' : dicom['paths']['path_to_simpsons_jpeg'],
                'path_to_simpsons_gif' : dicom['paths']['path_to_simpsons_gif'],
                'path_to_simpsons_webm' : dicom['paths']['path_to_simpsons_webm'],
            } 

            # append mask:
            masks.append(mask)
        
        except Exception as error:
            print('[ERROR]: %s' %error)
            
    # handle case where no views of given type have been found:   
    if views_data.empty:
        dicom = {'predicted_view' : None}

    if verbose:
        print("[@ %7.2f s] [PredictSegmentation]: Predicted [%s] segmentation" %(time()-start, dicom['predicted_view']))
    
    return masks



def post_process_single_apical_seg(mask):

    # create new directories:
    tools.CreateDirectory(mask['path_to_mask_jpeg'])
    tools.CreateDirectory(mask['path_to_mask_gif'])
    tools.CreateDirectory(mask['path_to_mask_webm'])
    tools.CreateDirectory(mask['path_to_simpsons_jpeg'])
    tools.CreateDirectory(mask['path_to_simpsons_gif'])
    tools.CreateDirectory(mask['path_to_simpsons_webm'])

    # collect post processing data:
    post_processing_metrics = tools.SegmentationApicalPostProcessing(mask)

    # parse results:
    post_processing_metrics['lvv_simpson'] = np.nan_to_num(post_processing_metrics['lvv_simpson'])
    post_processing_metrics['lvv_simpson'] = list(post_processing_metrics['lvv_simpson'])

    # build post processing object:
    post_processing_object = {
        'metrics': post_processing_metrics,
        'dicom_id': mask['dicom_id'],
    }

    # append data to list:
    return post_processing_object



def ProcessSegmentationResults(masks, view, verbose=False, start=time()):
    
    ''' Accepts masks array, returns dataframe with post processing data '''
    
    # predict on each frame:
    NUMBER_OF_THREADS = len(masks)

    if len(masks)>0:
        with Pool(NUMBER_OF_THREADS) as pool:
            post_processing_list = pool.map(post_process_single_apical_seg, masks)
            pool.close()
    else:
        post_processing_list = []
        
    # convert to dataframe:
    post_processing_data = pd.DataFrame(post_processing_list)
    post_processing_data.name = view + '_segmentation_data'
    
    if verbose:
        print("[@ %7.2f s] [ProcessSegmentationResults]: Processed [%s] segmentation results" %(time()-start, view))
    
    return post_processing_data