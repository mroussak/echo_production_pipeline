from Pipeline.Configuration.Configuration import configuration
from sagemaker.tensorflow.serving import Predictor
from Pipeline.Tools import Tools as tools
from collections import Counter
from scipy.ndimage import zoom
from decouple import config
import numpy as np
import sagemaker
import pydicom 
import pickle
import boto3
import sys
import cv2
import os



@tools.monitor_me()
def GetData(data_file_path):
    
    ''' Accepts data file path, returns object '''
    
    with open(data_file_path, 'rb') as handle:
        data = pickle.load(handle)
    
    return data
    
    
    
@tools.monitor_me()    
def PrepDataForModel(dicom, view):
    
    ''' Accepts dicom, view objects preps data for segmentation model '''
    
    # intialize variables:
    prepped_data = {
        'apical_view' : False,
        'input_to_model' : [],
    }
    apical_views = [
        'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
        'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
        'A5C',                      'A5C Zoomed Aorta',
    ]
    
    # exit if predicted view is not an apical view:
    if view['predicted_view'] not in apical_views:
        return prepped_data
        
    input_to_model = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # append to list:
        input_to_model.append(grayscale_image)
        
    # get resample ratios:
    frame_ratio = 20/dicom['pixel_data'].shape[0]
    height_ratio = 192/dicom['pixel_data'].shape[1]
    width_ratio = 128/dicom['pixel_data'].shape[2]
    
    # resample video:
    input_to_model = zoom(input_to_model, (frame_ratio, height_ratio, width_ratio))
    
    # prep input for model:
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    input_to_model = np.array([input_to_model.astype('float32')])
    input_to_model = pickle.dumps(input_to_model)
    
    # updated prepped_data dictionary:
    prepped_data['apical_view'] = True
    prepped_data['input_to_model'] = input_to_model
    
    return prepped_data
    
    

@tools.monitor_me()
def GetPrediction(prepped_data):
    
    ''' Accepts prepped data, returns prediction from segmentation model '''
    
    # initialize variables:
    prediction = {
        'apical_view' : False,
        'segmentation_mask' : [],
    }
    
    # exit if predicted view is not an apical view:
    if not prepped_data['apical_view']:
        return prediction
    
    # get endpoint of model:
    segmentation_predictor = Predictor('tf-multi-model-endpoint', model_name='', content_type='application/npy', serializer=None)

    # contact endpoint for prediction:
    segmentation_mask = np.array(segmentation_predictor.predict(prepped_data['input_to_model'])['predictions'])
    
    # update prediction dictionary:
    prediction['apical_view'] = True,
    prediction['segmentation_mask'] = segmentation_mask,
    
    return prediction
    
    

@tools.monitor_me()
def ParsePrediction(prediction):
    
    ''' Accepts segmentation prediction, parses data '''
    
    # initialize variables:
    parsed_prediction = {
        'apical_view' : False,
        'pixel_data' : [],
        'number_of_frames' : 0,
    }
    
    # exit if predicted view is not an apical view:
    if not prediction['apical_view']:
        return parsed_prediction
        
    return parsed_prediction
    


@tools.monitor_me()
def ExportSegmentationData(data, destination):
    
    ''' Accepts data, destination, saves data in .pkl format '''
    
    with open(destination, 'wb') as handle:
        pickle.dump(data, handle)
    
    
    