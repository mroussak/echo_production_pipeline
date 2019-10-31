from time import time



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