from Configuration.Configuration import kwargs 
from time import time
import pandas as pd



#def time_it(verbose=False):
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
                print("Script @ [%7.2f s]: Execution time [%7.2f s] for [%s]" %(end-start, end-function_start, function.__name__))
        
            return result
        
        return wrapper
    
    return decorator
    


def InitializeScript(script_name, verbose=False, start=time()):
                
    ''' Accepts script_name, prints title of script '''
        
    if verbose:
        print()
        print("[%s]___" %(script_name))
        
        


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
    
    
    
@time_it(**kwargs)    
def ReadDataFromFile(file, verbose=False, start=time()):
    
    ''' Accepts file path, returns data as dataframe,
        accepts .csv, .xlsx, .pkl, and .pickle files,
        throws exception otherwise '''
    
    if file[-3:] == "csv":
        data = pd.read_csv(file)
    elif file[-3:] == "pkl" or file[-6:] == "pickle":
        data = pd.read_pickle(file)
    elif file[-4:] == "xlsx":
        data = pd.read_excel(file)
    else:
        raise Exception("[ReadDataFromFile]: tried to read [%s], but file format not supported" %(file))

    if verbose:
        print("[@ %7.2f s] [ReadDataFromFile]: Read data from [%s]" %(time()-start, file))
            
    return data  
    
    

@time_it(**kwargs)
def ExportDataToFile(data, export_file, verbose=False, start=time()):
    
    ''' Accepts dataframe, export file, exports data to file '''
    
    # export table:
    if (export_file[-3:] == 'pkl') or (export_file[-6:] == 'pickle'):
        data.to_pickle(export_file)
        data_name = data.name
    elif export_file[-4:] == 'json':
        with open(export_file, 'w') as outfile:
            json.dump(data, outfile)
        data_name = 'json_object'
    elif export_file[-3:] == 'csv':
        data.to_csv(export_file, index=False)
        data_name = data.name
    else:
        raise Exception("[ExportDataToFile]: tried to read [%s], but file format not supported" %(file))
    
    if verbose:
        print("[@ %7.2f s] [ExportDataToFile]: Exported [%s] to [%s]" %(time()-start, data_name, export_file))   
        
        
        
def JoinDataFrames(data1, data2, on_index, new_name='unnamed_variable', verbose=False, start=time()):
    
    ''' Accepts two dataframes, returns data in joined datafame '''
    
    # join dataframes:
    data3 = data1.set_index(on_index)
    data4 = data2.set_index(on_index)
    data = data3.join(data4)
    data = data.reset_index()
    
    # name new dataframe:
    data.name = new_name
    
    if verbose:
        print("[@ %7.2f s] [JoinDataFrames]: Joined [%s] to [%s] as [%s]" %(time()-start, data2.name, data1.name, data.name))
    
    return data