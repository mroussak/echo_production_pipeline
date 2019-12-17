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
        'view_model_type' : 'video',
    },
}
