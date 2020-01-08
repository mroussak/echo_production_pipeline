from time import time

# Configuration:
configuration = {
    
    # monitor_me decorator tool configuration:
    'monitor_me' : {
        'monitor' : True,
        'verbose' : True,
        #'start' : time(),
        'arg_length' : 10,
        'traceback_lines' : 3,
    },
    
    # pipeline handlers configuration:
    'handlers' : {
        'log' : True,
    },
    
    # pipeline view configuration:
    'view' : {
        'preprocessing' : 'downsample',
        #'preprocessing' : 'zoom_cv2',
        #'preprocessing' : 'zoom',
        #'view_model_type' : 'frame',
        'view_model_type' : 'video',
        #'binary_model_type' : 'none',
        #'binary_model_type' : 'frame',
        'binary_model_type' : 'video',
    },
    
    # apical segmentation model configuration:
    'segmentation' : {
        'resample' : False,
        'frames' : 20,
    },
}
