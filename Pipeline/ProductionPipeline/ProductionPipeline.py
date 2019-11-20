#from Components.PericardialAbnormalitySUBA import PericardialAbnormalitySUBAPipeline
from Components.SegmentationApical import SegmentationApicalPipeline
from Components.SegmentationPSAX import SegmentationPSAXPipeline
from Components.Reports import ReportsPipeline
from Components.Dicoms import DicomsPipeline
from Components.Models import ModelsPipeline
from Components.Views import ViewsPipeline
from Tools import ProductionTools as tools
from decouple import config
from time import time
import sys
import os
import boto3
import botocore
BUCKET_NAME = config('AWS_S3_BUCKET_NAME')
client = boto3.client(
    's3',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
)
s3 = boto3.resource('s3')


def main(user_id='UserID1', session_id='SessionID1', s3_files=[], verbose=False, start=time()):

    # Variables:
    kwargs = {
        'verbose' : verbose,
        'start' : start,
    }

    # Directory tree:
    
    production_directory =  '/internal_drive/'
    user_directory = '/internal_drive/Users/' + user_id + '/'
    session_directory = 'Sessions/' + session_id + '/'
    file_paths = {
        'dicoms_directory' : user_directory + session_directory + 'Dicoms/',
        'dicoms_videos_directory' : user_directory + session_directory + 'Videos/Dicoms/',
        'videos_directory' : user_directory + session_directory + 'Videos/',
        'dicoms_table' : user_directory + session_directory + 'Tables/DicomsTable.pickle',
        'views_table' : user_directory + session_directory + 'Tables/ViewsTable.pickle',
        'segmentation_apical_table' : user_directory + session_directory + 'Tables/SegmentationApicalTable.pickle',
        'segmentation_psax_table' : user_directory + session_directory + 'Tables/SegmentationPSAXTable.pickle',
        'pericardial_abnormality_suba_table' : user_directory + session_directory + 'Tables/PericardialAbnormalitySUBATable.pickle',
        'reports' : user_directory + session_directory +'Reports/reports.json',
    }
    query_files = {
        'set_pipeline_start_time' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/PipelineQueries/set_pipeline_start_time.sql',
        'set_pipeline_complete_time' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/PipelineQueries/set_pipeline_complete_time.sql',
        'set_report_json_field' : config('BASE_DIR') + 'echo_production_pipeline/Database/EchoData/Queries/PipelineQueries/set_report_json_field.sql',
    }
    
    # System settings:
    sys.stdout = open(user_directory + session_directory + 'Reports/status.txt', 'w')
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
 
    
    ############
    ### TEMP ###
    
    # TODO: move file reader:
    for file in s3_files:
        s3.Bucket(BUCKET_NAME).download_file(file, file_paths['dicoms_directory'] + file)
    
    # TODO: move models pipeline to its own task:
    ModelsPipeline.main(**kwargs)
    
    ### ENDTEMP ###
    ###############
    
    # Step 1, commence pipeline:
    tools.InitializeScript(os.path.basename(__file__), **kwargs)
    tools.CommencePipeline(session_id, query_files['set_pipeline_start_time'], **kwargs)

    # Step 2, dicoms pipeline:
    DicomsPipeline.main(file_paths, **kwargs)

    # Step 3, views pipeline:
    ViewsPipeline.main(file_paths, **kwargs)

    # Step 4, model pipelines:
    SegmentationApicalPipeline.main(file_paths, **kwargs)
    SegmentationPSAXPipeline.main(file_paths, **kwargs)
    #PericardialAbnormalitySUBAPipeline.main(file_paths, **kwargs)

    # Step 5, reports pipeline:
    ReportsPipeline.main(file_paths, query_files, session_id, **kwargs)

    # Step 6, terminate script:
    tools.InitializeScript(os.path.basename(__file__), **kwargs)
    tools.TerminatePipeline(session_id, query_files['set_pipeline_complete_time'], **kwargs)



# Execute as standalone pipeline:
if __name__ == "__main__":
    
    # Variables:
    kwargs = {
        'verbose' : True,
        'start' : time(),
    }
    
    user_id = 'icardio'
    session_id = '1'
    
    # Step 1, load models if not already loaded:
    ModelsPipeline.main(**kwargs)

    # Step 2, build directory structure if needed:
    root_directory = tools.BuildRootDirectory(user_id, session_id)
    tools.BuildDirectoryTree(root_directory)
    
    # Step 3, execute pipeline:
    main(user_id, session_id, **kwargs)

    