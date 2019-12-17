from  Pipeline.Configuration.Configuration import configuration
from datetime import datetime
from time import time
import traceback



# Decorator tools:
def monitor_me(
    monitor = configuration['monitor_me']['monitor'],                    
    verbose = configuration['monitor_me']['verbose'], 
    start = time(),                                                   
    arg_length = configuration['monitor_me']['arg_length'], 
    traceback_lines = configuration['monitor_me']['traceback_lines']
    ):
    
    ''' time_it decorator, used to time execution time of functions '''
    
    def decorator(function):
        
        def wrapper(*args, **kwargs):
        
            # intialize result object:
            result = {}
        
            # if monitor is set to false, do nothing:
            if not monitor:
                
                result['content'] = function(*args, **kwargs)
                result['status'] = -1
                result['message'] = "Set 'monitor' to True in Configuration to enable monitorting"
                
                return result 
        
            # start timer:
            function_start = time()
            
            # try to execute function:
            try:
                result['content'] = function(*args, **kwargs)
                result['status'] = 0
                result['message'] = 'Success'
            
            except:
                result['content'] = None
                result['status'] = 1
                result['message'] = 'Failure [\n%s\n%s\n%s\n]' %(traceback.format_exc().splitlines()[-traceback_lines], traceback.format_exc().splitlines()[-2], traceback.format_exc().splitlines()[-1])
                
            # terminate timer:
            end = time()
            
            # print execution time when verbose is true:
            if verbose==True:
                if args:
                    
                    # shorten args for printing:
                    args = [str(arg)[0:arg_length] + '...' if len(str(arg))>arg_length else arg for arg in args ]
                    
                    result['message'] = "[%s] [Status: %s] [Message: %s] Script execution time [%7.2f s] Function execution time [%7.2f s] for [%s(%s)]" %(
                            datetime.now(), result['status'], result['message'], end-start, end-function_start, function.__name__, str(args)[1:-1]
                            )
                    
                    print(result['message'])
                
                else:
                    result['message'] = "[%s] [Status: %s] [Message: %s] Script execution time [%7.2f s] Function execution time [%7.2f s] for [%s()]" %(
                            datetime.now(), result['status'], result['message'], end-start, end-function_start, function.__name__
                            )
                            
                    print(result['message'])
        
            return result['content']
        
        return wrapper
    
    return decorator
    
