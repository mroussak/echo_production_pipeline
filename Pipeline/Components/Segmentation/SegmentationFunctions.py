from Mask_RCNN_serving2.mrcnn_serving_ready.inferencing import saved_model_config, saved_model_preprocess
#from mrcnn_serving_ready.inferencing import saved_model_config, saved_model_preprocess
from Pipeline.Configuration.Configuration import configuration
from sagemaker.tensorflow.serving import Predictor
from Pipeline.Tools import Tools as tools
from collections import Counter
from scipy.ndimage import zoom
from decouple import config
import numpy as np
import sagemaker
import traceback
import pydicom 
import pickle
import boto3
import math
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
def PrepDataForModel(dicom):
    
    ''' Accepts dicom, view objects preps data for segmentation model '''
    
    input_to_model = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # append to list:
        input_to_model.append(grayscale_image)
    
    # prep input for model:
    input_to_model = np.array(input_to_model)
    
    # resample video, spline + cv2 method:
    if configuration['segmentation']['resample']:
        
        new_number_of_frames = configuration['segmentation']['frames']
        
        frame_ratio = new_number_of_frames/dicom['pixel_data'].shape[0]
        height_ratio = 1
        width_ratio = 1
        
        input_to_model = zoom(input_to_model, (frame_ratio, height_ratio, width_ratio))
        
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    #input_to_model = np.array([input_to_model.astype('float32')])
    #input_to_model = pickle.dumps(input_to_model)
    
    model_config = saved_model_config.MY_INFERENCE_CONFIG
    preprocess_obj = saved_model_preprocess.ForwardModel(model_config)

    molded_images, image_metas, windows = preprocess_obj.mold_inputs(input_to_model)
    molded_images = molded_images.astype(np.float32)
    image_metas = image_metas.astype(np.float32)
    image_shape = molded_images[0].shape
    
    anchors = preprocess_obj.get_anchors(image_shape)
    anchors = np.broadcast_to(anchors, (input_to_model.shape[0],) + anchors.shape)
    
    prepped_data = {
        'raw_input' : input_to_model,
        'preprocess_obj' : preprocess_obj,
        'windows' : windows,
        'molded_images' : molded_images,
        'image_metas' : image_metas,
        'image_shape' : image_shape,
        'anchors' : anchors,
    }
    
    return prepped_data
    
    

@tools.monitor_me()
def GetPrediction(prepped_data):
    
    ''' Accepts prepped data, returns prediction from segmentation model '''
    
    # unpack prepped data:
    vid = prepped_data['raw_input']
    preprocess_obj = prepped_data['preprocess_obj']
    windows = prepped_data['windows']
    molded_images = prepped_data['molded_images']
    image_metas = prepped_data['image_metas']
    image_shape = prepped_data['image_shape']
    anchors = prepped_data['anchors']
    
    # get endpoint of model:
    predictor = Predictor('tf-multi-model-endpoint', model_name='Mask_RCNN_a4c_seg', content_type='application/dict',serializer=None)

    masks = []
    for idx in range(len(molded_images)):
        payload = {
            "instances": [
                {
                    "input_image": molded_images[idx,:,:,:].tolist(),
                    "input_image_meta": image_metas[idx,:].tolist(),
                    "input_anchors": anchors[idx,:,:].tolist()
                }
            ]
        }
        
        input_to_model = pickle.dumps(payload)
        
        prediction = predictor.predict(input_to_model)
        
        result = {
            'detection': np.array([prediction['predictions'][0]['mrcnn_detection/Reshape_1']]), 
            'mask': np.array([prediction['predictions'][0]['mrcnn_mask/Reshape_1']])
        }
        
        result_dict = preprocess_obj.result_to_dict(np.expand_dims(vid[idx], axis=0), molded_images, windows, result)[0]
        
        if result_dict['mask'].size!=0:
            mask = np.where(result_dict['mask'][:,:,0],255.0,0.0).astype(np.uint8)
            masks.append(mask)
        else:
            masks.append(np.zeros(vid[0].shape[:-1]))
            
    masks = np.array(masks)
 
    return masks
    
    

@tools.monitor_me()
def ParsePrediction(dicom, prediction):
    
    ''' Accepts segmentation prediction, parses data '''
    original_vid = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # append to list:
        original_vid.append(grayscale_image)
    
    original_vid = np.array(original_vid)
    number_of_frames = dicom['number_of_frames']
    seconds_per_frame = dicom['seconds_per_frame']
    
    # resample video, spline + cv2 method:
    if configuration['segmentation']['resample']:
        
        # update number of frames, seconds per frame:
        number_of_frames = configuration['segmentation']['frames']
        seconds_per_frame = seconds_per_frame * dicom['number_of_frames'] / number_of_frames
        
        # set resample ratios
        frame_ratio = number_of_frames/dicom['pixel_data'].shape[0]
        height_ratio = 1
        width_ratio = 1
        
        # resample video:
        original_vid = zoom(original_vid, (frame_ratio, height_ratio, width_ratio))
    
    # get masks:
    seg_video, simp_video = overlay_masks(original_vid, prediction)
    
    # pack result:
    parsed_prediction = {
        'segmentation' : {
            'pixel_data' : seg_video,
            'number_of_frames' : number_of_frames,
            'seconds_per_frame' : seconds_per_frame,
        },
        'simpsons' : {
            'pixel_data' : simp_video,
            'number_of_frames' : number_of_frames,
            'seconds_per_frame' : seconds_per_frame,
        },
        
    }
        
    return parsed_prediction



@tools.monitor_me()
def ExportSegmentationData(parsed_prediction, segmentation_data_destination, simpsons_data_destination):
    
    ''' Accepts parsed_prediction, destinations, saves parsed_prediction in .pkl format '''
    
    # unpack parsed prediction
    segmentation_data = parsed_prediction['segmentation']
    simpsons_data = parsed_prediction['simpsons']
    
    with open(segmentation_data_destination, 'wb') as handle:
        pickle.dump(segmentation_data, handle)
    
    with open(simpsons_data_destination, 'wb') as handle:
        pickle.dump(simpsons_data, handle)
        


def axis_of_symmetry(coords):
    cov = np.cov(coords)
    evals, evecs = np.linalg.eig(cov)
    sort_indices = np.argsort(evals)
    x_v1, y_v1 = evecs[:, sort_indices[0]]  # Eigenvector with largest eigenvalue
    x_v2, y_v2 = evecs[:, sort_indices[1]]
    theta = -np.arctan((y_v1)/(x_v1))  
    rotation_mat = np.matrix([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
    return(rotation_mat)

def apical_disks(mask, number_of_disks):
    coords = []
    y, x = np.nonzero(mask) 
    mean_x, mean_y = np.mean(x), np.mean(y)
    x, y = x - mean_x, y - mean_y                                
    rotation_mat = axis_of_symmetry(np.vstack([x, y]))
    transformed_mat = rotation_mat*np.vstack([x, y])
    x_transformed, y_transformed = transformed_mat.A
    ##Find top and bottom extremities using axis of symmetry
    max_y, min_y = max(y_transformed[np.where((x_transformed-0)<1)]), min(y_transformed[np.where((x_transformed-0)<1)]) 
    top_bottom_extremities = np.transpose(rotation_mat)*[[0,0],[min_y,max_y]]
    x_extremities, y_extremities = top_bottom_extremities.A[0]+mean_x, top_bottom_extremities.A[1]+mean_y
    coord_0, coord_1 = (int(x_extremities[0]), int(y_extremities[0])), (int(x_extremities[1]), int(y_extremities[1]))
    coords.append([coord_0,coord_1])
    # Find left and right extremities for all disks
    top_bottom_distance = max_y-min_y
    if top_bottom_distance>20:
        number_of_disks = number_of_disks
        disk_length = top_bottom_distance/number_of_disks
        for disk_num in range(1,number_of_disks+1):
            right_x = max(x_transformed[np.where(abs(y_transformed-(min_y+(disk_num)*disk_length))<1)])
            left_x = min(x_transformed[np.where(abs(y_transformed-(min_y+(disk_num)*disk_length))<1)])
            right_y =  y_transformed[np.where(x_transformed==right_x)]
            left_y =  y_transformed[np.where(x_transformed==left_x)]  
            left_right_extremities = np.transpose(rotation_mat)*[[left_x,right_x],[left_y,right_y]]
            x_extremities, y_extremities = left_right_extremities.A[0]+mean_x, left_right_extremities.A[1]+mean_y
            coord_0, coord_1 = (int(x_extremities[0]), int(y_extremities[0])), (int(x_extremities[1]), int(y_extremities[1]))
            coords.append([coord_0, coord_1])
        return(coords)
    else:
        raise Exception('length less than 20')
    
def overlay_masks(original_vid, masks):
    seg_video = []
    simp_video = []
    number_of_disks = 20
    for idx, mask in enumerate(masks):
        frame = original_vid[idx].astype(np.uint8)
        disk_volume = 0
        if (mask==0.0).all():
            seg_video.append(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
            simp_video.append(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
        else:   
    #         Using connected components
            mask = np.array(mask, dtype=np.uint8)
            ret, labels = cv2.connectedComponents(mask)
            (values,counts) = np.unique(labels,return_counts=True)
            values = values[1:]
            counts = counts[1:]
            ind=np.argmax(counts)
            mask = np.where(labels==values[ind],255.0,0.0)   
            mask = cv2.resize(mask, original_vid.shape[1:][::-1])
            mask = np.where(mask==0.0,0.0,255.0).astype(np.uint8)
            overlayed_mask = cv2.addWeighted(frame,1,mask,0.5,0)   
            seg_video.append(cv2.cvtColor(overlayed_mask,cv2.COLOR_GRAY2RGB))
            frame_for_simpsons = frame.copy()
            try:
                coords = apical_disks(mask, number_of_disks=number_of_disks)
                top_bottom_distance = math.sqrt(((1*(coords[0][1][0]-coords[0][0][0]))**2)+
                                                ((1*(coords[0][1][1]-coords[0][0][1]))**2)) 
                disk_length = top_bottom_distance/number_of_disks
                for coord in coords:
                    cv2.line(frame_for_simpsons,tuple(coord[0]),tuple(coord[1]),100,1) 
            except Exception as e:
                print(e)
            simp_video.append(cv2.cvtColor(frame_for_simpsons,cv2.COLOR_GRAY2RGB))
    seg_video = np.array(seg_video)  
    simp_video = np.array(simp_video)
    return seg_video, simp_video
    
    
    
# Decorator tools:
def am_i_apical():
    
    ''' am_i_apical decorator, used to execute segmentation pipeline for apical views or skip if otherwise '''
    
    def decorator(function):
        
        def wrapper(*args, **kwargs):

            try:
                
                # initialize variables:
                apical_views = [
                    'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
                    'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
                    'A5C',                      'A5C Zoomed Aorta',
                ]
                
                # get file paths object:
                if 'file_paths' in kwargs:
                    view_data_file = kwargs['file_paths']['view_data']
                else:
                    view_data_file = args[0]['view_data']

                # get view data object:                    
                with open(view_data_file, 'rb') as handle:
                    view_data = pickle.load(handle)

                # check if view is apical:
                if view_data['predicted_view'] in apical_views:
                    function(*args, **kwargs)
                
            except Exception as e:
                print('[ERROR] in [SegmentationPipeline]: Unable to determine view [%s]' %traceback.format_exc())
                
        return wrapper
    
    return decorator