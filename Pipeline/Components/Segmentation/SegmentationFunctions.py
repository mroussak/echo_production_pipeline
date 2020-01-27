from Mask_RCNN_serving.mrcnn_serving_ready.inferencing import saved_model_config, saved_model_preprocess
from Pipeline.Configuration.Configuration import configuration
from sagemaker.tensorflow.serving import Predictor
from Pipeline.Tools import Tools as tools
from collections import Counter
from scipy.ndimage import zoom
from datetime import datetime
from decouple import config
import numpy as np
import sagemaker
import traceback
import threading
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
        
    # add extra dimension to video:
    input_to_model = input_to_model.reshape(input_to_model.shape+(1,))
    
    # get Mask RCNN Serbving configuration:
    model_config = saved_model_config.MY_INFERENCE_CONFIG
    preprocess_object = saved_model_preprocess.ForwardModel(model_config)

    # build model objects:
    molded_images, image_metas, windows = preprocess_object.mold_inputs(input_to_model)
    anchors = preprocess_object.get_anchors(molded_images[0].shape)
    anchors = np.broadcast_to(anchors, (input_to_model.shape[0],) + anchors.shape)
    
    # pack data:
    prepped_data = {
        'original_video' : input_to_model,
        'preprocess_object' : preprocess_object,
        'windows' : windows,
        'molded_images' : molded_images,
        'image_metas' : image_metas,
        'anchors' : anchors,
    }
    
    return prepped_data
    
    

@tools.monitor_me()
def GetPrediction(prepped_data):
    
    ''' Accepts prepped data, returns prediction from segmentation model '''
    
    # unpack prepped data:
    original_video = prepped_data['original_video']
    preprocess_object = prepped_data['preprocess_object']
    windows = prepped_data['windows']
    molded_images = prepped_data['molded_images']
    image_metas = prepped_data['image_metas']
    anchors = prepped_data['anchors']
    
    # initialize variables:
    BATCH_SIZE = 50
    masks = []
    
    # get endpoint of model:
    predictor = Predictor('tf-multi-model-endpoint', model_name='Mask_RCNN_a4c_seg_batch50-compact-cpu', content_type='application/seg', serializer=None)
    
    # get number of frames, batches:
    number_of_frames = len(molded_images)
    number_of_missing_frames = 0
    number_of_batches = int(np.ceil(number_of_frames/BATCH_SIZE))
    
    # iterate over each batch:    
    for index in range(number_of_batches):
        
        # build payload batches:
        image_batch = molded_images[index*BATCH_SIZE:(index+1)*BATCH_SIZE, :, :, :]
        metas_batch = image_metas[index*BATCH_SIZE:(index+1)*BATCH_SIZE, :]
        anchor_batch = anchors[index*BATCH_SIZE:(index+1)*BATCH_SIZE, :, :]
        
        # set number of missing frames to 0:
        number_of_missing_frames = 0
        
        # pad batches smaller than batch size:
        if len(image_batch) < BATCH_SIZE:
            
            # get number of missing frames:
            number_of_missing_frames = BATCH_SIZE - len(image_batch)
            
            # build pads:
            extra_images = np.zeros((number_of_missing_frames, image_batch.shape[1], image_batch.shape[2], image_batch.shape[3]))
            extra_metas = np.zeros((number_of_missing_frames, metas_batch.shape[1]))
            extra_anchors = np.zeros((number_of_missing_frames, anchor_batch.shape[1], anchor_batch.shape[2]))
            
            # concatenate batch and pads:
            image_batch = np.concatenate((image_batch, extra_images))
            metas_batch = np.concatenate((metas_batch, extra_metas))
            anchor_batch = np.concatenate((anchor_batch, extra_anchors))
    
        # compile batch payload:
        batch_payload = {
            "molded_images": image_batch.astype(np.float16),
            "image_metas": metas_batch.astype(np.float16),
            "anchors": anchor_batch.astype(np.float16),
        }
        
        # serialize input:
        input_to_model = pickle.dumps(batch_payload)
        
        # get prediction:
        response = predictor.predict(input_to_model)
        
        for index in range(BATCH_SIZE - number_of_missing_frames):
            
            result = {
                'detection': np.array([response['predictions'][index]['mrcnn_detection/Reshape_50']]), 
                'mask': np.array([response['predictions'][index]['mrcnn_mask/Reshape_1']]),
            }
            
            result_dictionary = preprocess_object.result_to_dict(np.expand_dims(original_video[index], axis=0), molded_images, windows, result)[0]            
            
            if result_dictionary['mask'].size!=0:
                mask = np.where(result_dictionary['mask'][:,:,0],255.0,0.0).astype(np.uint8)
                masks.append(mask)
            else:
                masks.append(np.zeros(original_video[0].shape[:-1]))

    masks = np.array(masks, dtype=np.uint8)
    
    return masks
    


@tools.monitor_me()
def ParsePrediction(dicom, prediction):
    
    ''' Accepts segmentation prediction, parses data '''
    
    # initialize variables:
    original_vid = []
    
    # convert frames to grayscale and resize:
    for frame in dicom['pixel_data']:
        
        # convert frame to grayscale:
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # append to list:
        original_vid.append(grayscale_image)
    
    # prep original video for post processing:
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
    
    # check if the dicom contains meta data:
    if dicom['physical_units_x_direction'] is not None:
        
        # get masks and metrics:
        seg_video, simp_video, metrics = overlay_masks(original_vid, prediction, dicom)
        
    else:
        
        # get masks:
        seg_video, simp_video = overlay_masks(original_vid, prediction)
        metrics = None
    
    # pack result:
    parsed_prediction = {
        'segmentation' : {
            'pixel_data' : seg_video,
            'number_of_frames' : number_of_frames,
            'seconds_per_frame' : seconds_per_frame,
            'metrics' : metrics,
        },
        'simpsons' : {
            'pixel_data' : simp_video,
            'number_of_frames' : number_of_frames,
            'seconds_per_frame' : seconds_per_frame,
            'metrics' : metrics,
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
    
def overlay_masks(original_vid, masks, meta_data=None):
    seg_video = []
    simp_video = []
    if meta_data:      
        lv_diam = []
        lvv_simpson = []
    number_of_disks = 20
    for idx, mask in enumerate(masks):
        frame = original_vid[idx].astype(np.uint8)
        disk_volume = 0
        if (mask==0.0).all():
            seg_video.append(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
            simp_video.append(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
            if meta_data:      
                lv_diam.append(np.nan)                
                lvv_simpson.append(np.nan)
        else:   
    #         Using connected components
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
                if meta_data:
                    lv_diams = []
                    for coord in coords[1:]:
                        diam = math.sqrt(((meta_data['physical_delta_x']*(coord[1][0]-coord[0][0]))**2)+
                                                    ((meta_data['physical_delta_y']*(coord[1][1]-coord[0][1]))**2)) 
                        lv_diams.append(diam)
                        disk_volume += np.pi*((diam/2)**2)*disk_length*meta_data['physical_delta_y']
                    lv_diam.append(max(lv_diams))                
                    lvv_simpson.append(disk_volume)             
            except Exception as e:
                print(e)
                if meta_data:
                    lv_diam.append(np.nan)                
                    lvv_simpson.append(np.nan)
            simp_video.append(cv2.cvtColor(frame_for_simpsons,cv2.COLOR_GRAY2RGB))
    seg_video = np.array(seg_video)  
    simp_video = np.array(simp_video)
    if meta_data:
#         lvv_simpson = medfilt(lvv_simpson)
        lvdd = max(lv_diam)
        lvsd = min(lv_diam)
        lvdv = max(lvv_simpson)
        lvsv = min(lvv_simpson)
        ef = (1-lvsv/lvdv)*100
    if meta_data:
        return seg_video, simp_video, {'lvv_simpson' : lvv_simpson,'lvdd' : lvdd,'lvsd' : lvsd,'lvdv' : lvdv, 'lvsv' : lvsv, 'ef' : ef}
    else:
        return seg_video, simp_video
    
    
    
# Decorator tools:
def am_i_apical():
    
    ''' am_i_apical decorator, used to execute segmentation pipeline for apical views or skip if otherwise '''
    
    def decorator(function):
        
        def wrapper(*args, **kwargs):

            try:
                
                # initialize variables:
                apical_views = ['A2C', 'A4C', 'A4C Zoomed LV']
                # apical_views = [
                #     'A2C',                      'A2C Zoomed Mitral',        'A3C',                  'A3C Zoomed Aorta',
                #     'A4C',                      'A4C Zoomed LV',            'A4C Zoomed Mitral',    'A4C Zoomed RV',
                #     'A5C',                      'A5C Zoomed Aorta',
                # ]
                
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