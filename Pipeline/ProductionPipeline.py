from time import time
from Tools import ProductionTools as tools
from Components.Dicoms import DicomsPipeline
from Components.Views import ViewsPipeline
from Components.SegmentationApical import SegmentationApicalPipeline
from Components.SegmentationPSAX import SegmentationPSAXPipeline
from Components.Reports import ReportsPipeline

import global_vars
import os
import sys
# sys.stdout = open('/internal_drive/echo_production_pipeline/Flask/static/status.txt', 'w')

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())

def main(start=time()):

    # Variables:
    verbose = True

    # Directory tree:
    production_directory =  '/internal_drive/'
    file_paths = {
        'dicoms_directory' : production_directory + 'Dicoms/',
        # 'dicoms_directory' : production_directory + 'Dicoms_Anon/4/',
        'dicoms_videos_directory' : production_directory + 'Videos/Dicoms/',
        'videos_directory' : production_directory + 'Videos/',
        'dicoms_table' : production_directory + 'Tables/DicomsTable.pickle',
        'views_table' : production_directory + 'Tables/ViewsTable.pickle',
        'segmentation_apical_table' : production_directory + 'Tables/SegmentationApicalTable.pickle',
        'segmentation_psax_table' : production_directory + 'Tables/SegmentationPSAXTable.pickle',
        # 'views_model' : production_directory + 'Models/Views/ViewsModel.keras',
        # 'segmentation_model_apical_configuration' : production_directory + 'Models/SegmentationApical/SegmentationConfigurationApical.yaml',
        # 'segmentation_model_psax_configuration' : production_directory + 'Models/SegmentationPSAX/SegmentationConfigurationPSAX.yaml',
        # 'a4c_segmentation_model' : production_directory + 'Models/SegmentationApical/SegmentationModelA4C.keras',
        # 'a2c_segmentation_model' : production_directory + 'Models/SegmentationApical/SegmentationModelA2C.keras',
        # 'psax_model' : production_directory + 'Models/SegmentationPSAX/SegmentationModelPSAX.keras',
        'reports' : production_directory + 'Reports/reports.json',
        #'reports' : production_directory + 'echo_production_pipeline/Flask/static/reports.json',
    }

    # Step 1, dicoms pipeline:
    DicomsPipeline.main(file_paths, verbose, start)

    # Step 2, views pipeline:
    ViewsPipeline.main(file_paths, verbose, start)

    # Step 3, segmentation pipelines:
    SegmentationApicalPipeline.main(file_paths, verbose, start)
    SegmentationPSAXPipeline.main(file_paths, verbose, start)

    # Step 3, reports pipeline:
    ReportsPipeline.main(file_paths, verbose, start)

    # Step 4, terminate script:
    tools.TerminateScript()



if __name__ == "__main__":
    global_vars.init()
    process_start_time = time()
    main(start=time())
    print('process took :',(time()-process_start_time)/60, 'minutes')