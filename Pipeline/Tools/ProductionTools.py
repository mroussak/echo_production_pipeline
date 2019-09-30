import os
import json
import pandas as pd
from time import time
from Tools.EchoPipelineTools import load_video as LoadVideo
from Tools.EchoPipelineTools import view_postprocessing as ViewsPostProcessing
from Tools.EchoPipelineTools import seg_postprocessing_apical as SegmentationApicalPostProcessing 
from Tools.EchoPipelineTools import seg_postprocessing_psax as SegmentationPSAXPostProcessing



def InitializeScript(script_name, verbose=False, start=time()):
                
    ''' Accepts script_name, prints title of script '''
        
    if verbose:
        print("|__")
        print("[%s]___" %(script_name))
        
    

def TerminateScript():
                
    ''' Prints termination message '''
        
    print('Done')
        
        
        
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
    
    
    
def JoinDataFrames(data1, data2, on_index, verbose=False, start=time()):
    
    ''' Accepts two dataframes, returns data in joined datafame '''
    
    # handle empty dataframes:
    if data1.empty:
                
        if verbose:
            print("[@ %7.2f s] [JoinDataFrames]: [%s] empty, returning [%s]" %(time()-start, data1.name, data2.name))
            
        return data2
            
    if data2.empty:
    
        if verbose:
            print("[@ %7.2f s] [JoinDataFrames]: [%s] empty, returning [%s]" %(time()-start, data2.name, data1.name))
        
        return data1
    
    # join dataframes:
    data3 = data1.set_index(on_index)
    data4 = data2.set_index(on_index)
    data = data3.join(data4)
    data = data.reset_index()
    
    # name new dataframe:
    data.name = data1.name
    
    if verbose:
        print("[@ %7.2f s] [JoinDataFrames]: Joined [%s] to [%s]" %(time()-start, data2.name, data1.name))
    
    return data
    

    
def ConcatDataFrames(data1, data2, verbose=False, start=time()):

    ''' Accepts two dataframes, returns concatenated dataframe '''

    data = pd.concat([data1, data2])
    data = data.reset_index()
    data.name = data1.name
    
    if verbose:
        print("[@ %7.2f s] [ConcatDataFrames]: Concatenated [%s] to [%s]" %(time()-start, data2.name, data1.name))
        
    return data



def CreateDirectory(directory_name, verbose=False, start=time()):
    
    ''' Accepts directory name, creates directory if it does not exist '''
    
    try:
        os.makedirs(directory_name)
    except:
        pass
    
    if verbose:
        print("[@ %7.2f s] [CreateDirectory]: Created directory [%s]" %(time()-start, directory_name))
        
        
        
        
        