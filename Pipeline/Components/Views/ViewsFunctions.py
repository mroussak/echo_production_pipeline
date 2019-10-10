import global_vars
import os
import cv2
from time import time
import pandas as pd
import numpy as np
import Tools.ProductionTools as tools
from multiprocessing import Pool
from itertools import repeat

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def ParseDicomData(dicom_data, verbose=False, start=time()):
    
    ''' Accepts dicom data, returns parsed dicom data '''
    
    #dicom_data = tools.GetItemsFromList(dicom_data, 'dicom_type', 'standard')
    dicom_data = dicom_data.loc[dicom_data['dicom_type'] == 'standard']
    dicom_data.name = 'dicom_data'

    if len(dicom_data) == 0:
        raise(ValueError('No standard views found'))
    
    if verbose:
        print("[@ %7.2f s] [ParseDicomData]: Parsed dicom_data" %(time()-start))
        
    return dicom_data


def PredictViews(dicom_data, verbose=False, start=time()):
    ''' Accepts dicom data, model, returns predictions as dataframe '''

    # initialize variables:
    predictions = []

    # predict on each frame:
    # print('predicting w views model')
    # start_time = time()
    for index, dicom in dicom_data.iterrows():
        # load videos:
        frames = tools.LoadVideo(dicom['paths']['path_to_dicom_jpeg'], img_type='jpg', normalize='frame')
        frames = frames.reshape(frames.shape + (1,))

        # predict view:
        with global_vars.graph.as_default():
            prediction = global_vars.views_model.predict(frames, verbose=0)

        # build prediction object:
        prediction_object = {
            'dicom_id': dicom['dicom_id'],
            'predictions': prediction,
        }

        predictions.append(prediction_object)
    # print('predicting w views model took : ', time() - start_time, 'seconds')

    if verbose:
        print("[@ %7.2f s] [PredictView]: Predicted views on [%d] videos" % (time() - start, len(predictions)))

    return predictions

def post_process_single_view(prediction):
    # post processing:
    prediction = tools.ViewsPostProcessing(prediction)

    # build object:
    post_processing_object = {
        'view_details': prediction,
        'predicted_view': prediction['predicted_view'],
        'video_view_threshold': prediction['video_view_threshold'],
        'dicom_id': prediction['dicom_id'],
    }

    return post_processing_object


def ProcessViewsPredictions(predictions, verbose=False, start=time()):
    
    ''' Accepts predictions from views model, returns processed results '''
    
    # predict on each frame:
    NUMBER_OF_THREADS = len(predictions)

    with Pool(NUMBER_OF_THREADS) as pool:
        post_processing_list = pool.map(post_process_single_view, predictions)
        pool.close()
        
    # convert list to dataframe:
    post_processing_data = pd.DataFrame(post_processing_list)
        
    # only return usable views:
    #post_processing_data = post_processing_data.loc[post_processing_data['usable_view']==True]
    
    # name dataframe:
    post_processing_data.name = 'views_post_processing_data'
    
    if verbose:
        print("[@ %7.2f s] [ProcessViewPredictions]: Processed predictions" %(time()-start))
    
    return post_processing_data

