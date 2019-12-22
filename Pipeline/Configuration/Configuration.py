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
        'log' : False,
    },
    'models' : {
        #'view_model_type' : 'frame',
        'view_model_type' : 'video',
        #'view_model_type' : 'spline',
        'binary_model_type' : 'none',
        #'binary_model_type' : 'frame',
        #'binary_model_type' : 'video',
        #'binary_model_type' : 'spline',
    },
}
