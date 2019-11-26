import Tools.DatabaseTools as tools
from time import time, sleep
import pandas as pd
import hashlib
import os



@tools.time_it(**tools.kwargs)
def GetRootFolders():

    ''' Returns list of root folders '''
    
    root_folders = [
        '/labelling_app/2017_Studies_For_View_Labelling/extracted_data/2017_studies_extracted_anon_crop/Acuson_Cypress/dim_480_640/Standard',
        '/labelling_app/2017_Studies_For_View_Labelling/extracted_data/2017_studies_extracted_anon_crop/Vivid_i/dim_422_636/Standard',
        '/labelling_app/2018_studies_extracted_anon_crop/Terason/dim_650_880/Standard',
        '/labelling_app/2018_studies_extracted_anon_crop/Vivid_i/dim_422_636/Standard',
        '/labelling_app/2018_studies_extracted_anon_crop/Vivid_iq/dim_708_1016/Standard',
        '/labelling_app/2019_studies_extracted_anon_crop/Terason/dim_650_880/Standard',
        '/labelling_app/2019_studies_extracted_anon_crop/Vivid_i/dim_422_636/Standard',
        '/labelling_app/2019_studies_extracted_anon_crop/Vivid_iq/dim_708_1016/Standard',
        ]    

    return root_folders



@tools.time_it(**tools.kwargs)
def GetFilePaths(root_paths):

    ''' Accepts list of root_folders, returns list of file paths as dataframe '''

    # intialize variables:
    videos_table = pd.DataFrame(columns=['object_id', 'path_to_jpegs'])

    for root_path in root_paths:

        visits = os.listdir(root_path)
        
        for visit in visits:
            
            root_folder = visit
            visit_path = root_path + '/' + visit
            
            videos = os.listdir(visit_path)
            
            for video in videos:
            
                object_id = root_folder + '_' + video
                video_path = visit_path + '/' + video
                
                video_entry = {
                    'object_id' : object_id,
                    'path_to_jpegs' : video_path,
                    }
                
                videos_table = videos_table.append(video_entry, ignore_index=True)

    return videos_table



@tools.time_it(**tools.kwargs)
def RenameJpegs(videos_table):
    
    ''' Accepts vidoes table, renames all files with leading zeros for webm builder '''
    
    for index, row in videos_table.iterrows():
    
        path = row['path_to_jpegs']
    
        for file in os.listdir(path):
            old_name = os.path.join(path,file)
            new_name = os.path.join(path,file.zfill(8))
            os.rename(old_name, new_name)



@tools.time_it(**tools.kwargs)
def ParseVideosTable(videos_table):
    
    ''' Accepts raw videos_table, returns parsed videos_table '''
    
    # split id field:
    videos_table[['patient_hash', 'visit_date', 'folder']] = videos_table['object_id'].str.split('_', expand=True)
    
    # create unique id:
    videos_table['object_id'] = videos_table['object_id'].map(lambda x: x.encode('utf-8'))
    videos_table['object_id'] = videos_table['object_id'].map(lambda x: hashlib.sha224(x).hexdigest())
    
    # clean date field:
    videos_table['visit_date'] = videos_table['visit_date'].map(lambda x: x.rstrip('.fsv'))
    
    # name dataframe:
    videos_table.name = 'videos_table'
    
    return videos_table
    
    