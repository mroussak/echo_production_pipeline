from time import time



def GetKeyWordArgs():
    
    ''' key word argument builder '''
    
    kwargs = {
        'vebrose' : True,
        'start' : time(),
    }

    return kwargs



def time_it(verbose=False):
    
    ''' time_it decorator, used to time execution time of functions '''
    
    def decorator(function):
        
        def wrapper(*args, **kwargs):
        
            # start timer:
            start = time()
            
            # execute function:
            result = function(*args, **kwargs)
            
            # terminate timer:
            end = time()
            
            # print execution time when verbose is true:
            if verbose==True:
                print("Execution time [%7.2f s] for [%s]" %(end-start, function.__name__))
        
            return result
        
        return wrapper
    
    return decorator
    


def QueryType(query, verbose=False, start=time()):
    
    ''' Accepts query, returns query type as string '''
    
    # intialize variables:
    query_type = '[ERROR] UNDEFINED'
    
    if query[0:6] == 'SELECT':
        query_type = 'SELECT'
    
    if query[0:6] == 'INSERT':
        query_type = 'INSERT'

    if query[0:6] == 'CREATE':
        query_type = 'CREATE'
        
    if query[0:5] == 'ALTER':
        query_type = 'ALTER'
        
    if verbose:
        print('[@ %7.2f s] [GetQueryType]: Found query with type [%s]' %(time()-start, query_type))
    
    return query_type