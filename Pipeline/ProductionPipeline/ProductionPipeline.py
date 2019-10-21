# Script imports:
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

def main(user_id='UserID1', session_id='SessionID1', start=time()):

    # Variables:
    kwargs = {
        'verbose' : True,
        'start' : start,
    }
    
    # System settings:
    #sys.stdout = open('/internal_drive/echo_production_pipeline/Flask/static/status.txt', 'w')
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Directory tree:
    production_directory =  '/internal_drive/'
    user_directory = '/internal_drive/Users/' + user_id + '/'
    session_directory = 'Sessions/' + session_id + '/'
    file_paths = {
        'dicoms_directory' : user_directory + session_directory + 'Dicoms/',
        #'dicoms_directory' : production_directory + 'Dicoms_Anon/9/',
        'dicoms_videos_directory' : user_directory + session_directory + 'Videos/Dicoms/',
        'videos_directory' : user_directory + session_directory + 'Videos/',
        'dicoms_table' : user_directory + session_directory + 'Tables/DicomsTable.pickle',
        'views_table' : user_directory + session_directory + 'Tables/ViewsTable.pickle',
        'segmentation_apical_table' : user_directory + session_directory + 'Tables/SegmentationApicalTable.pickle',
        'segmentation_psax_table' : user_directory + session_directory + 'Tables/SegmentationPSAXTable.pickle',
        'reports' : user_directory + session_directory +'Reports/reports.json',
        #'reports' : production_directory + 'echo_production_pipeline/Flask/static/reports.json',
    }

    # Step 1, dicoms pipeline:
    DicomsPipeline.main(file_paths, **kwargs)

    # Step 2, views pipeline:
    ViewsPipeline.main(file_paths, **kwargs)

    # Step 3, segmentation pipelines:
    SegmentationApicalPipeline.main(file_paths, **kwargs)
    SegmentationPSAXPipeline.main(file_paths, **kwargs)

    # Step 3, reports pipeline:
    ReportsPipeline.main(file_paths, **kwargs)

    # Step 4, terminate script:
    tools.TerminateScript()



# Execute as standalone pipeline:
if __name__ == "__main__":
    
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    
    # Step 1, load models if not already loaded:
    ModelsPipeline.main(start=time())
    
    # Step 2, execute pipeline:
    main(user_id='UserID1', session_id='SessionID1', start=time())
    
    