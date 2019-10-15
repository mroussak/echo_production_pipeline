import keras.models as km
import tensorflow as tf
from time import time
import importlib
import yaml



def PrepSegmentationModel(configuration_file, verbose=False, start=time()):

    ''' Accepts configuration_file, returns segmentation_metrics '''

    # open and read file:
    with open(configuration_file, 'r') as tfile:
        file_str = tfile.read()
    config = yaml.load(file_str)  # yaml.load(file_str, Loader=yaml.FullLoader)

    # pull metrics:
    tpr_loss = importlib.import_module(config['loss']).tpr_loss_coefficient(smooth=0)
    dice_loss = importlib.import_module(config['loss']).dice_loss_coefficient(smooth=0)
    iou_metric_coeff = importlib.import_module(config['metrics']).iou_metric_coeff(0.05, 0.04)
    tpr_metric_coeff = importlib.import_module(config['metrics']).tpr_metric_coeff(0.05, 0.04)
    fpr_metric_coeff = importlib.import_module(config['metrics']).fpr_metric_coeff(0.05, 0.04)

    # pack metrics:
    segmentation_metrics = {
        'dice_coefficient': dice_loss,
        'iou': iou_metric_coeff,
        'tpr': tpr_metric_coeff,
        'fpr': fpr_metric_coeff,
    }

    if verbose:
        print('[@ %7.2f s] [PrepSegmentationModel]: Prepped model using [%s]' %(time()-start, configuration_file))

    return segmentation_metrics
    
    

def InitializeModel(model_file, model_configuration, verbose=False, start=time()):

    ''' Accepts model_file, model_configuration, returns loaded model '''

    # load models:
    if model_configuration == None:
        model_variable = km.load_model(model_file)
    else:
        model_variable = km.load_model(model_file, model_configuration)
   
    if verbose:
        print('[@ %7.2f s] [InitializeModel]: Loaded model from [%s]' %(time()-start, model_file))
        
    return model_variable