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
import math
import sys
import cv2
import os
from Pipeline.Tools.EchoPipelineTools import load_video


@tools.monitor_me()
def GetDicomData(dicom_data_file_path):
    
    ''' Accepts dicom data file path, returns dicom object '''
    
    with open(dicom_data_file_path, 'rb') as handle:
        dicom = pickle.load(handle)
    
    return dicom
    
    

@tools.monitor_me()    
def PrepDataForModel(dicom, file_paths):    

    preprocessing = configuration['models']['preprocessing']

    # downsample:
    if preprocessing == 'downsample':
        return PrepDataForModel_downsample(dicom, file_paths)
    
    # spline + cv2:
    if preprocessing == 'zoom_cv2':
        return PrepDataForModel_zoom_cv2(dicom)
    
    # spline only:
    if preprocessing == 'zoom':
        return PrepDataForModel_zoom(dicom)



def PrepDataForModel_downsample(dicom, file_paths):

    # intialize variables:
    input_to_model = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # resize image: 
        resized_image = cv2.resize(grayscale_image, (192,128))
    
        # append to list:
        input_to_model.append(resized_image)
    
    # downsample model:
    delims = [math.floor(i*len(input_to_model)/20) for i in list(range(1,20))]
    input_to_model = np.array([i[0] for i in np.array_split(input_to_model, delims)])
    
    # prep input for model:
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    input_to_model = np.array([input_to_model.astype('float32')])
    input_to_model = pickle.dumps(input_to_model)

    return input_to_model



def PrepDataForModel_zoom_cv2(dicom):

    # intialize variables:
    input_to_model = []
    prediction = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # resize image: 
        resized_image = cv2.resize(grayscale_image, (192,128))
    
        # append to list:
        input_to_model.append(resized_image)
    
    # resample video, spline + cv2 method:
    frame_ratio = 20/dicom['pixel_data'].shape[0]
    height_ratio = 1
    width_ratio = 1
    input_to_model = zoom(input_to_model, (frame_ratio, height_ratio, width_ratio))
    
    # prep input for model:
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    input_to_model = np.array([input_to_model.astype('float32')])
    input_to_model = pickle.dumps(input_to_model)

    return input_to_model



def PrepDataForModel_zoom(dicom):

    # intialize variables:
    input_to_model = []
    prediction = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        input_to_model.append(grayscale_image)
    
    # resample video, spline method:
    frame_ratio = 20/dicom['pixel_data'].shape[0]
    height_ratio = 128/dicom['pixel_data'].shape[2]
    width_ratio = 192/dicom['pixel_data'].shape[1]
    input_to_model = zoom(input_to_model, (frame_ratio, height_ratio, width_ratio))

    # prep input for model:
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    input_to_model = np.array([input_to_model.astype('float32')])
    input_to_model = pickle.dumps(input_to_model)

    return input_to_model



@tools.monitor_me()
def GetPrediction(input_to_model):

    if configuration['models']['view_model_type'] == 'frame':
        prediction = GetPrediction_frame(input_to_model)
        
    elif configuration['models']['view_model_type'] == 'video':
        prediction = GetPrediction_video(input_to_model)
        
    return prediction
    
    
    
def GetPrediction_frame(input_to_model):
    
    ''' Accepts dicom, return prediction from model '''
    
    # # intialize variables:
    # input_to_model = []
    # prediction = []
    
    # # convert frames to grayscale and resize:
    # for frame in dicom['pixel_data']:
        
    #     # convert frame to grayscale:
    #     grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
    #     # reduce frame size:
    #     reduced_image = cv2.resize(grayscale_image,(96*2,64*2))
        
    #     # append to list:
    #     input_to_model.append(reduced_image)
    
    # # convert data to numpy array for further processing:
    # input_to_model = np.array(input_to_model)
    
    # # reshape video to fit model requirements:
    # number_of_frames = input_to_model.shape[0]
    # means = input_to_model.reshape(number_of_frames, -1).mean(-1)
    # stds = input_to_model.reshape(number_of_frames, -1).std(-1)
    # input_to_model = input_to_model - means[:, np.newaxis, np.newaxis]
    # input_to_model = input_to_model / stds[:, np.newaxis, np.newaxis]
    # input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    
    # input_to_model = pickle.dumps(input_to_model.astype('float16'))
    
    if configuration['models']['binary_model_type'] == 'None':
    
        # get endpoint of model:
        views_predictor = Predictor('tf-multi-model-endpoint', model_name='views_model', content_type='application/npy', serializer=None)

    elif configuration['models']['binary_model_type'] == 'frame':

        # get endpoint of model:
        views_predictor = Predictor('tf-multi-model-endpoint', model_name='master_model', content_type='application/npy', serializer=None)

    # contact endpoint for prediction:
    result = np.array(views_predictor.predict(input_to_model)['predictions'])
    
    # build prediction object:
    prediction = {
        'model_name' : model_name,
        'predictions' : result,
    }
    
    return prediction
    
    
    
def GetPrediction_video(input_to_model):
    
    ''' Accepts input_to_model, returns prediction from model '''
    
    # intitalize variables:
    preprocessing = configuration['models']['preprocessing']
    
    # get endpoint of model:
    if configuration['models']['binary_model_type'] == 'none':

        # models:    
        model_name = 'ResNet50V2_views_model_vid_spline'
        #model_name = 'ResNet50V2_views_model_vid_spline_noweights'

        # get endpoint of model:
        views_predictor = Predictor('tf-multi-model-endpoint', model_name=model_name, content_type='application/npy', serializer=None)

    elif configuration['models']['binary_model_type'] == 'video':

        # models:
        if preprocessing == 'downsample':
            model_name = 'ResNet50V2_master_model_vid_dows'
        elif preprocessing == 'zoom_cv2' or preprocessing == 'zoom':
            model_name = 'ResNet50V2_master_model_vid_spline'
        
        # get endpoint of model:
        views_predictor = Predictor('tf-multi-model-endpoint', model_name=model_name, content_type='application/npy', serializer=None)

    # contact endpoint for prediction:
    result = np.array(views_predictor.predict(input_to_model)['predictions'])
    
    # build prediction object:
    prediction = {
        'model_name' : model_name,
        'predictions' : result,
    }
    
    return prediction
    


@tools.monitor_me()
def ParsePrediction(dicom_id, prediction):

    # get model configuration:
    views_model = configuration['models']['view_model_type']
    binary_model = configuration['models']['binary_model_type']

    # use frame model:
    if views_model == 'frame' and binary_model == 'none':
        result = ParsePrediction_view_only_frame_level(dicom_id, prediction)
        
    elif views_model == 'frame' and binary_model == 'frame':
        result = ParsePrediction_view_and_binary_frame_level(dicom_id, prediction)
        
    elif views_model == 'video' and binary_model == 'none':
        result = ParsePrediction_view_only_video_level(dicom_id, prediction)
        
    elif views_model == 'video'  and binary_model == 'video':
        result = ParsePrediction_view_and_binary_video_level(dicom_id, prediction)
        
    return result



def ParsePrediction_view_only_frame_level(dicom_id, prediction):
    
    unique_views = [
        'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
        'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
        'A5C',                      'A5C Zoomed Aorta',         'PLAX',                 'PLAX Aortic Cusps',
        'PLAX Mitral Cusps',        'PLAX Paricardial',         'PSAX Apex',            'PSAX Mitral', 
        'PSAX Papillary',           'PSAXA',                    'PSAXA Pulmonary',      'PSAXA Zoomed Aorta',
        'PSAXA Zoomed Tricuspid',   'RVIT',                     'SUB IVC',              'SUB Short Axis',           
        'SUBCOSTAL',                'Suprasternal',
    ]
    
    # unpack prediction object:
    predictions = prediction['predictions']
    model_name = prediction['model_name']
    
    # intialize variables:
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
        'view_model_type' : configuration['models']['view_model_type'],
        'binary_model_type' : configuration['models']['binary_model_type'],
        'model_name' : model_name,
    }
    
    return result



def ParsePrediction_view_and_binary_frame_level(dicom_id, prediction):

    unique_views = [
        'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
        'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
        'A5C',                      'A5C Zoomed Aorta',         'PLAX',                 'PLAX Aortic Cusps',
        'PLAX Mitral Cusps',        'PLAX Paricardial',         'PSAX Apex',            'PSAX Mitral', 
        'PSAX Papillary',           'PSAXA',                    'PSAXA Pulmonary',      'PSAXA Zoomed Aorta',
        'PSAXA Zoomed Tricuspid',   'RVIT',                     'SUB IVC',              'SUB Short Axis',           
        'SUBCOSTAL',                'Suprasternal',
    ]
    abnormalities = ['abnormal','normal']
    
    # unpack prediction object:
    predictions = prediction['predictions']
    model_name = prediction['model_name']
    
    # intialize variables:
    max_view_confidences = []
    max_abnormality_confidences = []
    view_predictions = []
    abnormality_predictions = []

    # find prediction of each frame:
    for prediction in predictions:
        
        # get the value with the highest confidence and its index:
        max_view_value = max(prediction['score0'])
        max_abnormality_value = max(prediction['score1'])
        max_view_value_index = np.argmax(prediction['score0'])
        max_abnormality_value_index = np.argmax(prediction['score1'])
        
        # append the highest confidence to the list;
        max_view_confidences.append(max_view_value)
        max_abnormality_confidences.append(max_abnormality_value)
        
        # get the predicted view and append to the list:
        predicted_view = unique_views[max_view_value_index]
        predicted_abnormality = abnormalities[max_abnormality_value_index]
        view_predictions.append(predicted_view)
        abnormality_predictions.append(predicted_abnormality)
    
    # get the view that was predicted most often:
    most_common_view = Counter(view_predictions).most_common(1)[0][0]
    
    # calculate how many times the most common view was predicted as a perecent of total predictions:
    most_common_view_probability = Counter(view_predictions).most_common(1)[0][1]/len(view_predictions)
    
    # get the probability of the most common view on each frame:
    probs_winning_class = np.array(max_view_confidences)[np.where(np.array(view_predictions) == most_common_view)[0]]
    
    # calculate frame_view_threshold metric:
    frame_view_threshold = np.std(probs_winning_class)/np.mean(probs_winning_class)
    
    # determine if abnormality is present:
    total_abnormal_frames = 0
    for abnormality_prediction in abnormality_predictions:
        if abnormality_prediction == 'abnormal':
            total_abnormal_frames += 1
    
    # report abnormality if at least 20% of the frames are abnormal:
    if total_abnormal_frames/len(abnormality_predictions) > 0.2:
        abnormality = True
    else:
        abnormality = False
    
    # determine if view is usable:
    if (most_common_view_probability>0.5) & (frame_view_threshold<0.1):
        usable_view = True
    else:
        usable_view = False
    
    # extract abnormality predictions:
    abnormality_predictions = []
    for prediction in predictions:
        abnormality_predictions.append(prediction['score1'])
    
    # split abnormality predictions into normal and abnormals:
    normal_prediction_scores, abnormal_prediction_scores = zip(*abnormality_predictions)
    
    # convert to numpy arrays:
    normal_scores = np.array(normal_prediction_scores)
    abnormal_scores = np.array(abnormal_prediction_scores)
    
    if abnormality:
    
        # get the length of twenty percent of the dataset:
        twenty_percent = int(len(abnormal_scores) * 0.2)
        
        # get the values of the largest 20%:
        largest_values = abnormal_scores[np.argsort(abnormal_scores)[-twenty_percent:]]
        
        # get mean of 20% largest values
        abnormality_confidence = largest_values.mean()
            
    elif not abnormality:
        
        # get the mean of the normal scores:
        abnormality_confidence = normal_scores.mean()
    
    result = {
        'dicom_id' : dicom_id,
        'predicted_view' : most_common_view, 
        'abnormality' : abnormality,
        'frame_view_threshold' : frame_view_threshold, 
        'view_confidence' : most_common_view_probability,
        'abnormality_confidence' : abnormality_confidence,
        'usable_view' : usable_view,
        'view_model_type' : configuration['models']['view_model_type'],
        'binary_model_type' : configuration['models']['binary_model_type'],
        'model_name' : model_name,
    }
    
    return result
    


def ParsePrediction_view_only_video_level(dicom_id, prediction):
    
    # initialize variables:
    unique_views = [
        'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
        'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
        'A5C',                      'A5C Zoomed Aorta',         'PLAX',                 'PLAX Aortic Cusps',
        'PLAX Mitral Cusps',        'PLAX Paricardial',         'PSAX Apex',            'PSAX Mitral', 
        'PSAX Papillary',           'PSAXA',                    'PSAXA Pulmonary',      'PSAXA Zoomed Aorta',
        'PSAXA Zoomed Tricuspid',   'RVIT',                     'SUB IVC',              'SUB Short Axis',           
        'SUBCOSTAL',                'Suprasternal',
    ]
    
    # unpack prediction object:
    predictions = prediction['predictions']
    model_name = prediction['model_name']
    
    # get max confidence value, index:
    max_confidence = max(predictions[0])
    max_confidence_index = np.argmax(predictions[0])
    
    # determine view:
    predicted_view = unique_views[max_confidence_index]
    
    # determine if view is usable:
    if max_confidence > 0.5:
        usable_view = True
    else:
        usable_view = False
    
    result = {
        'dicom_id' : dicom_id,
        'predicted_view' : predicted_view, 
        'view_confidence' : max_confidence,
        'usable_view' : usable_view,
        'view_model_type' : configuration['models']['view_model_type'],
        'binary_model_type' : configuration['models']['binary_model_type'],
        'model_name' : model_name,
        'abnormality_confidence' : 'none',
    }   
    
    return result



def ParsePrediction_view_and_binary_video_level(dicom_id, prediction):
    
    # intialize variables:
    unique_views = [
        'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
        'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
        'A5C',                      'A5C Zoomed Aorta',         'PLAX',                 'PLAX Aortic Cusps',
        'PLAX Mitral Cusps',        'PLAX Paricardial',         'PSAX Apex',            'PSAX Mitral', 
        'PSAX Papillary',           'PSAXA',                    'PSAXA Pulmonary',      'PSAXA Zoomed Aorta',
        'PSAXA Zoomed Tricuspid',   'RVIT',                     'SUB IVC',              'SUB Short Axis',           
        'SUBCOSTAL',                'Suprasternal',
    ]
    abnormalities = ['abnormal','normal']
    
    # unpack prediction object:
    predictions = prediction['predictions']
    model_name = prediction['model_name']
    
    # get max confidence value, index:
    max_view_confidence = max(predictions[0]['score0'])
    max_abnormality_confidence = max(predictions[0]['score1'])
    
    max_view_confidence_index = np.argmax(predictions[0]['score0'])
    max_abnormality_confidence_index = np.argmax(predictions[0]['score1'])
    
    # determine view:
    predicted_view = unique_views[max_view_confidence_index]
    predicted_abnormality = abnormalities[max_abnormality_confidence_index]
    
    # determine if view is usable:
    if max_view_confidence > 0.5:
        usable_view = True
    else:
        usable_view = False
    
    result = {
        'dicom_id' : dicom_id,
        'predicted_view' : predicted_view, 
        'predicted_abnormality' : predicted_abnormality,
        'view_confidence' : max_view_confidence,
        'abnormality_confidence' : max_abnormality_confidence,
        'usable_view' : usable_view,
        'view_model_type' : configuration['models']['view_model_type'],
        'binary_model_type' : configuration['models']['binary_model_type'],
        'model_name' : model_name,
    }   
    
    return result

    

@tools.monitor_me()
def ExportPrediction(prediction, destination):
    
    ''' Accepts prediction, destination, saves data in .pkl format '''
    
    with open(destination, 'wb') as handle:
        pickle.dump(prediction, handle)
    
    
    