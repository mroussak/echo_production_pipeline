import Components.Models.ModelsFunctions as funcs
import Tools.ProductionTools as tools
import tensorflow as tf
from time import time
import os



def main(verbose=False, start=time()):
    
    # Variables:
    global views_model 
    global a4c_segmentation_model
    global a2c_segmentation_model
    global psax_segmentation_model
    global graph 
    graph = tf.get_default_graph()
    kwargs = {
        'verbose' : verbose,
        'start' : start,
    }
    
    # Directory tree:
    root_directory ='/internal_drive/Models/'
    file_paths = {
        'apical_configuration_file' : root_directory + '/SegmentationApical/SegmentationConfigurationApical.yaml',
        'psax_configuration_file' : root_directory + '/SegmentationPSAX/SegmentationConfigurationPSAX.yaml',
        'suba_configuration_file' : root_directory + '/PericardialAbnormalitySUBA/PericardialAbnormalityConfigurationSUBA.yaml',
        'views_model' : root_directory + '/Views/ViewsModel.keras',
        'a2c_segmenation_model' : root_directory + '/SegmentationApical/SegmentationModelA2C.keras',
        'a4c_segmenation_model' : root_directory + '/SegmentationApical/SegmentationModelA4C.keras', 
        'psax_segmentation_model' : root_directory + '/SegmentationPSAX/SegmentationModelPSAX.keras',
        'suba_pericardial_abnormality_model' : root_directory + '/PericardialAbnormalitySUBA/PericardialAbnormalityModelSUBA.keras',
    }
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), verbose, start)

    # Step 2, prep models:
    apical_configuration = funcs.PrepSegmentationModel(file_paths['apical_configuration_file'], **kwargs)
    psax_configuration = funcs.PrepSegmentationModel(file_paths['psax_configuration_file'], **kwargs)
    suba_configuration = funcs.PrepPericardialAbnormalityModel(file_paths['suba_configuration_file'], **kwargs)
    
    # Step 3, intialize models:
    views_model = funcs.InitializeModel(file_paths['views_model'], None, **kwargs)
    a2c_segmentation_model = funcs.InitializeModel(file_paths['a2c_segmenation_model'], apical_configuration, **kwargs)
    a4c_segmentation_model = funcs.InitializeModel(file_paths['a4c_segmenation_model'], apical_configuration, **kwargs)
    psax_segmentation_model = funcs.InitializeModel(file_paths['psax_segmentation_model'], psax_configuration, **kwargs)
    #suba_pericardial_abnormality_model = funcs.InitializeModel(file_paths['suba_pericardial_abnormality_model'], suba_configuration, **kwargs)




