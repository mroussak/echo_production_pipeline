import Tools.DatabaseTools as tools
from time import time, sleep
import multiprocessing
import pandas as pd
import hashlib
import ffmpeg
import os



@tools.time_it(**tools.kwargs)
def BuildManuallyAddedDataTable(videos_table):
    
    ''' Accepts videos_table, returns manually_added_data_table '''
    
    # intialize variables:
    video_root_path = '/internal_drive/Videos/'
    manually_added_data_table = pd.DataFrame()
    
    # create primary key:
    manually_added_data_table['object_id'] = videos_table['object_id'].map(lambda x: x.encode('utf-8'))
    manually_added_data_table['object_id'] = manually_added_data_table['object_id'].map(lambda x: hashlib.sha224(x).hexdigest())
    
    # get foreign key:
    manually_added_data_table['video_id'] = videos_table['object_id']
    
    # copy jpeg path:
    manually_added_data_table['path_to_jpegs'] = videos_table['path_to_jpegs']
    
    # create webm path:
    manually_added_data_table['path_to_dicom_webm'] = video_root_path + manually_added_data_table['object_id'] + '.webm'
    
    # name dataframe:
    manually_added_data_table.name = 'manually_added_data_table'
    
    return manually_added_data_table
    


def BuildSingleWebm(dicom):
        
        ''' Accepts dicom, builds single webm file '''
        
        try:
            
            # unpack dicom:
            input_files = dicom['input_files']
            output_file = dicom['output_file']
            
            # skip if file already exists:
            if os.path.exists(output_file):
                return 
            
            # ffmpeg parameters:
            framerate = 30
            output_options = {
                "format": "webm",
                "pix_fmt": "yuv420p",
                "video_bitrate": 1000000,
                # "-i": os.path.join(clean_dir, '%%01d.jpg')
                # "crf": 10,
            }
      
            # build webm:
            (ffmpeg
                .input(input_files, pattern_type="glob", framerate=framerate)
                .output(output_file, **output_options)
                .global_args('-loglevel', 'quiet', '-y')
                .run()
            )
            
        except Exception as error:
            print('[ERROR] in [build_single_video]: [%s]' %error)
            
    

@tools.time_it(**tools.kwargs)
def BuildWebmFiles(manually_added_data_table):
    
    ''' Accepts dicom data, builds webms '''
        
    # create list of webms:
    list_of_webms = []
    
    for index, row in manually_added_data_table.iterrows():
        
        # general:
        input_files = row['path_to_jpegs'] + '/*.jpg'
        output_file = row['path_to_dicom_webm']
        dicom = {'input_files' : input_files, 'output_file' : output_file}
        list_of_webms.append(dicom)
    
    # multiprocessing, build each webm file in its own thread:
    number_of_threads = multiprocessing.cpu_count()
    
    with multiprocessing.Pool(number_of_threads) as pool:
        
        # multiprocess:
        total_vidoes = pool.map(BuildSingleWebm, list_of_webms)
        
        
        
        

        