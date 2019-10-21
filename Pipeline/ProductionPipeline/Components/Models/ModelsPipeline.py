import Components.Models.ModelsFunctions as funcs
import Tools.ProductionTools as tools
import tensorflow as tf
from time import time
import os

conf = tf.ConfigProto()
conf.gpu_options.allow_growth=True
session = tf.Session(config=conf)

def main(start=time()):

    # Variables:
    global views_model 
    global a4c_segmentation_model
    global a2c_segmentation_model
    global psax_segmentation_model
    global graph 
    graph = tf.get_default_graph()
    verbose = True
    kwargs = {
        'verbose' : True,
        'start' : start,
    }
    
    # Directory tree:
    root_directory ='/internal_drive/Models/'
    file_paths = {
        'apical_configuration_file' : root_directory + '/SegmentationApical/SegmentationConfigurationApical.yaml',
        'psax_configuration_file' : root_directory + '/SegmentationPSAX/SegmentationConfigurationPSAX.yaml',
        'views_model' : root_directory + '/Views/ViewsModel.keras',
        'a2c_segmenation_model' : root_directory + '/SegmentationApical/SegmentationModelA2C.keras',
        'a4c_segmenation_model' : root_directory + '/SegmentationApical/SegmentationModelA4C.keras', 
        'psax_segmentation_model' : root_directory + '/SegmentationPSAX/SegmentationModelPSAX.keras',
    }
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)

    # Step 2, prep models:
    apical_configuration = funcs.PrepSegmentationModel(file_paths['apical_configuration_file'], **kwargs)
    psax_configuration = funcs.PrepSegmentationModel(file_paths['psax_configuration_file'], **kwargs)
    
    # Step 3, intialize models:
    views_model = funcs.InitializeModel(file_paths['views_model'], None, **kwargs)
    a2c_segmentation_model = funcs.InitializeModel(file_paths['a2c_segmenation_model'], apical_configuration, **kwargs)
    a4c_segmentation_model = funcs.InitializeModel(file_paths['a4c_segmenation_model'], apical_configuration, **kwargs)
    psax_segmentation_model = funcs.InitializeModel(file_paths['psax_segmentation_model'], psax_configuration, **kwargs)

    # Step 4, terminate script:
    tools.TerminateScript()
