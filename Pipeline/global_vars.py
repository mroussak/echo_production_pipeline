import yaml
import importlib
import keras.models as km
import tensorflow as tf

def PrepSegmentationModel(configuration_file, verbose=False):
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

    return segmentation_metrics

def init():

    global views_model
    global a4c_seg_model
    global a2c_seg_model
    global psax_seg_model

    global graph
    graph = tf.get_default_graph()

    apical_seg_metrics = PrepSegmentationModel('/internal_drive/Models/SegmentationApical/SegmentationConfigurationApical.yaml')
    psax_seg_metrics = PrepSegmentationModel('/internal_drive/Models/SegmentationPSAX/SegmentationConfigurationPSAX.yaml')

    #Load Models
    views_model = km.load_model('/internal_drive/Models/Views/ViewsModel.keras')
    a2c_seg_model = km.load_model('/internal_drive/Models/SegmentationApical/SegmentationModelA2C.keras', custom_objects=apical_seg_metrics)
    a4c_seg_model = km.load_model('/internal_drive/Models/SegmentationApical/SegmentationModelA4C.keras', custom_objects=apical_seg_metrics)
    psax_seg_model = km.load_model('/internal_drive/Models/SegmentationPSAX/SegmentationModelPSAX.keras', custom_objects=psax_seg_metrics)