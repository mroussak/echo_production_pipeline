from time import time
import sys
import os

# Pipeline imports:
sys.path.insert(1, '/internal_drive/echo_production_pipeline/Pipeline/ProductionPipeline/')
from Components.Models import ModelsPipeline
import Tools.ProductionTools as tools
import ProductionPipeline


# Main:
if __name__ == "__main__":
    
    
    ''' Test new dicoms '''
    
    # intialize variables:
    user_id = 'Demo'
    session_id = 'Tests'
    
    # Step 1, load models if not already loaded:
    ModelsPipeline.main(start=time())
    
    # Step 2, build directory structure if needed:
    root_directory = tools.BuildRootDirectory(user_id, session_id)
    tools.BuildDirectoryTree(root_directory)
    
    # Step 3, execute pipeline:
    ProductionPipeline.main(user_id, session_id, start=time())
    
    
        
    ''' Run new models on demo data '''
    
    # # intialize variables:
    # user_id = 'Demo'
    # session_ids = range(0,15)
    
    # # Step 1, load models if not already loaded:
    # ModelsPipeline.main(start=time())
    
    # for session_id in session_ids:
        
    #     # correct data type:
    #     session_id = str(session_id)
        
    #     # Step 2, build directory structure if needed:
    #     root_directory = tools.BuildRootDirectory(user_id, session_id)
    #     tools.BuildDirectoryTree(root_directory)
        
    #     # Step 3, execute pipeline:
    #     ProductionPipeline.main(user_id, session_id, start=time())