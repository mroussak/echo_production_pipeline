#from Components.PericardialAbnormalitySUBA import PericardialAbnormalitySUBAPipeline
from Components.SegmentationApical import SegmentationApicalPipeline
from Components.SegmentationPSAX import SegmentationPSAXPipeline
from Components.Reports import ReportsPipeline
from Components.Dicoms import DicomsPipeline
from Components.Models import ModelsPipeline
from Components.Views import ViewsPipeline
from Tools import ProductionTools as tools
from time import time
import sys
import os



def main(user_id='UserID1', session_id='SessionID1', verbose=False, start=time()):

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
    
    # System settings:
    #sys.stdout = open(user_directory + session_directory + 'Reports/status.txt', 'w')
    sys.stdout = open('/sandbox/dsokol/echo_production_pipeline/Applications/iCardioAI/static/Users/daniel@icardio.ai/Sessions/1/Reports/status.txt', 'w')
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
    

    # Step 1, dicoms pipeline:
    DicomsPipeline.main(file_paths, **kwargs)

    # Step 2, views pipeline:
    ViewsPipeline.main(file_paths, **kwargs)

    # Step 3, model pipelines:
    SegmentationApicalPipeline.main(file_paths, **kwargs)
    SegmentationPSAXPipeline.main(file_paths, **kwargs)
    #PericardialAbnormalitySUBAPipeline.main(file_paths, **kwargs)

    # Step 4, reports pipeline:
    ReportsPipeline.main(file_paths, **kwargs)

    # Step 5, terminate script:
    tools.TerminateScript()



# Execute as standalone pipeline:
if __name__ == "__main__":
    
    # Variables:
    kwargs = {
        'verbose' : True,
        'start' : time(),
    }
    
    user_id = 'UserID1'
    session_id = 'SessionID1'
    
    # Step 1, load models if not already loaded:
    ModelsPipeline.main(**kwargs)

    # Step 2, build directory structure if needed:
    root_directory = tools.BuildRootDirectory(user_id, session_id)
    tools.BuildDirectoryTree(root_directory)
    
    # Step 3, execute pipeline:
    main(user_id, session_id, **kwargs)

    