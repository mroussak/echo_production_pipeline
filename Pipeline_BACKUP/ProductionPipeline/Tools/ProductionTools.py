from Tools.EchoPipelineTools import seg_postprocessing_apical as SegmentationApicalPostProcessing 
from Tools.EchoPipelineTools import seg_postprocessing_psax as SegmentationPSAXPostProcessing
from Tools.EchoPipelineTools import view_postprocessing as ViewsPostProcessing
from Tools.EchoPipelineTools import load_video as LoadVideo
from datetime import datetime
from decouple import config
from time import time
import pandas as pd
import json
import sys
import os

# Database imports:
sys.path.insert(1, config("BASE_DIR") + 'echo_production_pipeline/Database/EchoData/')
import PostgresCaller



def InitializeScript(script_name, verbose=False, start=time()):
                
    ''' Accepts script_name, prints title of script '''
        
    if verbose:
        print()
        print("[%s]___" %(script_name))
        
    

def CommencePipeline(visit_id, query_file, verbose=False, start=time()):
    
    ''' Accepts visit_id, query_file, commences pipeline '''
    
    parameters = {
        'visit_id' : int(visit_id),
        'started_processing_at_time' : datetime.now()
    }
    
    PostgresCaller.main(query_file, parameters)
    
    if verbose:
        print('[@ %7.2f s] [CommencePipeline]: Commenced pipeline' %(time()-start))
        
        

def TerminatePipeline(visit_id, query_file, verbose=False, start=time()):
                
    ''' Accepts visist id, query file, terminates pipeline '''
        
    parameters = {
        'visit_id' : int(visit_id),
        'processed_at_time' : datetime.now()
    }
        
    PostgresCaller.main(query_file, parameters)
        
    if verbose:
        print('[@ %7.2f s] [TerminatePipeline]: Terminated pipeline' %(time()-start))
    
        
        
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
    
    
    
def JoinDataFrames(data1, data2, on_index, new_name='unnamed_variable', verbose=False, start=time()):
    
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
    data.name = new_name
    
    if verbose:
        print("[@ %7.2f s] [JoinDataFrames]: Joined [%s] to [%s] as [%s]" %(time()-start, data2.name, data1.name, data.name))
    
    return data
    

    
def ConcatDataFrames(data1, data2, new_name='unnamed_variable', verbose=False, start=time()):

    ''' Accepts two dataframes, returns concatenated dataframe '''

    data = pd.concat([data1, data2], sort=False)
    data = data.reset_index()
    data.name = new_name
    
    if verbose:
        print("[@ %7.2f s] [ConcatDataFrames]: Concatenated [%s] to [%s] as [%s]" %(time()-start, data2.name, data1.name, data.name))
        
    return data



def CreateDirectory(directory_name, verbose=False, start=time()):
    
    ''' Accepts directory name, creates directory if it does not exist '''
    
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    
    if verbose:
        print("[@ %7.2f s] [CreateDirectory]: Created directory [%s]" %(time()-start, directory_name))
        
        
        
def ValueExistsInTable(data, key, value, verbose=False, start=time()):
    
    ''' Accepts table as dataframe, key, value, returns true if the value exists 
        in the table or false otherwise '''
    
    result = (data[key] == value).any()

    if verbose:
        print("[@ %7.2f s] [ValueExistsInTable]: Value [%s] exists in [%s] -> [%s]" %(time()-start, value, data.name, result))
        
    return result
    


def BuildGif(path_to_jpeg_folder, path_to_gif, verbose=False, start=time()):
    
    ''' Accepts path to jpeg folder, path to gifs, builds gifs from jpegs
        and saves gif at path to gifs '''
    
    # build directories to store gifs:
    tools.CreateDirectory(path_to_gif)
    
    # load video:
    video = LoadVideo(path_to_jpeg, normalize=False, img_type='jpg', image_dim=None)
    
    # create gifs:
    imageio.mimsave(path_to_gif, video)
       
    if verbose:
        print("[@ %7.2f s] [BuildGif]: Built gif at [%s]" %(time()-start, path_to_gif))
        


def GetItemsFromList(dictionary_list, key, value, verbose=False, start=time()):
    
    ''' Accepts list of dictionaries, key, value, returns subset list of dictionaries '''
    
    # intialize variables:
    new_list = []
    
    for item in dictionary_list:
        
        if item[key] == value:
            new_list.append(item)
    
    if verbose:
        print("[@ %7.2f s] [GetItemsFromList]: Found [%d] items with [%s] = [%s]" %(time()-start, len(new_list), key, value))
    
    return new_list
    
    
    
def BuildRootDirectory(user_id, session_id, verbose=False):
    
    ''' Accepts user_id, session_id, builds root directory '''
    
    root_directory = '/internal_drive/Users/' + user_id + '/Sessions/' + session_id + '/'
    
    if verbose:
        print('[BuildRootDirectory]: Built root directory [%s]' %root_directory)
        
    return root_directory
    
    

def BuildDirectoryTree(root_directory, verbose=False):
    
    ''' Accepts root directory, builds directory structure '''
    
    if not os.path.exists(root_directory):
    
        videos_directory = root_directory + 'Videos/'
        tables_directory = root_directory + 'Tables/'
        reports_directory = root_directory + 'Reports/'
        dicoms_directory = root_directory + 'Dicoms/'
        
        os.makedirs(videos_directory)
        os.makedirs(tables_directory)
        os.makedirs(reports_directory)
        os.makedirs(dicoms_directory)
    
    if verbose:
        print('[BuildDirectoryTree]: Built directory tree')