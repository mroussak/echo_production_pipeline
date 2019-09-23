from time import time
from Tools import ProductionTools as tools
from Components.Dicoms import DicomsPipeline
from Components.Dicoms import DicomsFunctions
from Components.Views import ViewsPipeline
from Components.Views import ViewsFunctions
from Components.Segmentation import SegmentationPipeline
from Components.Segmentation import SegmentationFunctions
from Components.Reports import ReportsPipeline
from Components.Reports import ReportsFunctions



def main(start=time()):
    
    # Variables:
    verbose = True
    
    # directory tree:
    production_directory =  '/internal_drive/Production/'
    file_paths = {
        'dicoms_directory' : production_directory + 'Dicoms/',
        'dicoms_videos_directory' : production_directory + 'Videos/Dicoms/',
        'videos_directory' : production_directory + 'Videos/',
        'dicoms_table' : production_directory + 'Tables/DicomsTable.pickle',
        'views_table' : production_directory + 'Tables/ViewsTable.pickle',
        'segmentation_table' : production_directory + 'Tables/SegmentationTable.pickle',
        'views_model' : production_directory + 'Models/Views/ViewsModel.keras',
        'segmentation_model_configuration' : production_directory + 'Models/Segmentation/SegmentationConfiguration.yaml',
        'a4c_segmentation_model' : production_directory + 'Models/Segmentation/A4CSegmentationModel.keras',
        'a2c_segmentation_model' : production_directory + 'Models/Segmentation/A2CSegmentationModel.keras',
        'reports' : production_directory + 'Reports/reports.json',        
    }
    
    # Step 1, dicoms pipeline:
    DicomsPipeline.main(file_paths, verbose, start)
    
    # Step 2, views pipeline:
    ViewsPipeline.main(file_paths, verbose, start)
    
    # Step 3, segmentation pipeline:
    SegmentationPipeline.main(file_paths, verbose, start)
    
    # Step 3, reports pipeline:
    ReportsPipeline.main(file_paths, verbose, start)
    
    # Step 4, terminate script:
    tools.TerminateScript()
    
    
    
if __name__ == "__main__":
    main(start=time())