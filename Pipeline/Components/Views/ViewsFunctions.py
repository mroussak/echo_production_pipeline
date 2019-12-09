from sagemaker.tensorflow.serving import Predictor
from Tools import Tools as tools
from collections import Counter
from decouple import config
import numpy as np
import pydicom 
import pickle
import boto3
import sys
import cv2
import os



@tools.monitor()
def GetDicomData(dicom_data_file_path):
    
    ''' Accepts dicom data file path, returns dicom object '''
    
    with open(dicom_data_file_path, 'rb') as handle:
        dicom = pickle.load(handle)
    
    return dicom
    

@tools.monitor()    
def GetPrediction(dicom):
    
    ''' Accepts dicom, return prediction from model '''
    
    # intialize variables:
    input_to_model = []
    prediction = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # reduce frame size:
        reduced_image = cv2.resize(grayscale_image,(96*2,64*2))
        
        # append to list:
        input_to_model.append(reduced_image)
    
    # convert data to numpy array for further processing:
    input_to_model = np.array(input_to_model)
    
    # reshape video to fit model requirements:
    number_of_frames = input_to_model.shape[0]
    means = input_to_model.reshape(number_of_frames, -1).mean(-1)
    stds = input_to_model.reshape(number_of_frames, -1).std(-1)
    input_to_model = input_to_model - means[:, np.newaxis, np.newaxis]
    input_to_model = input_to_model / stds[:, np.newaxis, np.newaxis]
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    
    input_to_model = pickle.dumps(input_to_model.astype('float16'))
    
    # get endpoint of model:
    views_predictor = Predictor('tf-multi-model-endpoint', model_name='views_model', content_type='application/npy',serializer=None)
    
    # contact endpoint for prediction:
    prediction = np.array(views_predictor.predict(input_to_model)['predictions'])
    
    return prediction
    
    

@tools.monitor()
def ParsePrediction(dicom_id, predictions):
    
    # intialize variables:
    unique_views = [
        'A2C',                      'A2C Zoomed Mitral',    'A3C',                  'A3C Zoomed Aorta', 
        'A4C','A4C Zoomed LV',      'A4C Zoomed Mitral',    'A4C Zoomed RV',        'A5C',
        'A5C Zoomed Aorta',         'PLAX',                 'PLAX Aortic Cusps',    'PLAX Mitral Cusps', 
        'PLAX Paricardial',         'PSAX',                 'PSAX Apex',            'PSAX Mitral', 
        'PSAX Papillary',           'PSAXA',                'PSAXA Pulminary',      'PSAXA Zoomed Aorta', 
        'PSAXA Zoomed Tricuspid',   'RVIT',                 'SUB IVC',              'SUB Short Axis', 
        'SUBCOSTAL',                'Suprasternal',         'Unclear Dark',         'Unclear Noisy'
    ]
    max_confidences = []
    view_predictions = []
    
    # find prediction of each frame:
    for prediction in predictions:
        
        # get the value with the highest confidence and its index:
        max_value = max(prediction)
        max_value_index = np.argmax(prediction)
        
        # append the highest confidence to the list;
        max_confidences.append(max_value)
        
        # get the predicted view and append to the list:
        predicted_view = unique_views[max_value_index]
        view_predictions.append(predicted_view)
    
    # get the view that was predicted most often:
    most_common_view = Counter(view_predictions).most_common(1)[0][0]
    
    # calculate how many times the most common view was predicted as a perecent of total predictions:
    most_common_view_probability = Counter(view_predictions).most_common(1)[0][1]/len(view_predictions)
    
    # get the probability of the most common view on each frame:
    probs_winning_class = np.array(max_confidences)[np.where(np.array(view_predictions) == most_common_view)[0]]
    
    # calculate frame_view_threshold metric:
    frame_view_threshold = np.std(probs_winning_class)/np.mean(probs_winning_class)
    
    # determine if view is usable:
    if (most_common_view_probability>0.5) & (frame_view_threshold<0.1):
        usable_view = True
    
    else:
        usable_view = False
    
    result = {
        'dicom_id' : dicom_id,
        'predicted_view' : most_common_view, 
        'frame_view_threshold' : frame_view_threshold, 
        'video_view_threshold' : most_common_view_probability,
        'usable_view' : usable_view,
    }
    
    return result
    
    

@tools.monitor()
def ExportPrediction(prediction, destination):
    
    ''' Accepts prediction, destination, saves data in .pkl format '''
    
    with open(destination, 'wb') as handle:
        pickle.dump(prediction, handle)
    
    
    