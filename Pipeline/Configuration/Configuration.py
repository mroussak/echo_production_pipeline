from time import time

# Configuration:
configuration = {
    'monitor_me' : {
        'monitor' : True,
        'verbose' : True,
        #'start' : time(),
        'arg_length' : 10,
        'traceback_lines' : 3,
    },
    'handlers' : {
        'log' : True,
    },
    'models' : {
        'preprocessing' : 'downsample',
        #'preprocessing' : 'zoom_cv2',
        #'preprocessing' : 'zoom',
        #'view_model_type' : 'frame',
        'view_model_type' : 'video',
        #'binary_model_type' : 'none',
        #'binary_model_type' : 'frame',
        'binary_model_type' : 'video',
    },
}
