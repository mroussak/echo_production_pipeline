from time import time




def time_it(verbose=False, start=time()):
    
    ''' time_it decorator, used to time execution time of functions '''
    
    def decorator(function):
        
        def wrapper(*args, **kwargs):
        
            # start timer:
            function_start = time()
            
            # execute function:
            result = function(*args, **kwargs)
            
            # terminate timer:
            end = time()
            
            # print execution time when verbose is true:
            if verbose==True:
                if args:
                    
                    # shorten args for printing:
                    args = [str(arg)[0:10] + '...' if len(str(arg))>10 else arg for arg in args ]
                    
                    print("Script @ [%7.2f s]: Execution time [%7.2f s] for [%s(%s)]" %(end-start, end-function_start, function.__name__, str(args)[1:-1] ))
                
                else:
                    print("Script @ [%7.2f s]: Execution time [%7.2f s] for [%s()]" %(end-start, end-function_start, function.__name__))
        
            return result
        
        return wrapper
    
    return decorator
    
    
    
def exception_handler(verbose=False):
    
    ''' time_it decorator, used to time execution time of functions '''
    
    def decorator(function):
        
        def wrapper(*args, **kwargs):
        
            # try:
            try:
                
                # execute function:
                result = function(*args, **kwargs)
            
                status = 0
                message = '[%s] Success' %function.__name__
            
            except Exception as exception:
                
                status = 1
                message = 'Failure [%s]' %exception
            
            if verbose:
                print('[%s] [Status: %s] [Message: %s]' %(function.__name__, status, message))
                
            return (result, status, message)
        
        return wrapper
    
    return decorator
    
    
    

def ExportDicom(dicom, status, verbose=False, start=time()):
    
    ''' Accepts dicom, status, returns dicom ready for export '''
    
    export_dicom = {
        'dicom' : dicom,
        'status' : status,
    }
    
    if verbose:
        print('[@ %7.2f s] [ExportDicom]: Exported dicom object' %(time()-start))
    
    return export_dicom