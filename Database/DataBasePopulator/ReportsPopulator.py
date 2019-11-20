from Components.ReportsReader import ReportsReaderPipeline
from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
from time import time
import os



# Main:
def main():
    
    # Directory tree:
    file_paths = {
        'reports_table' : '/labelling_app/patient_descriptors.csv',
        'descriptors' : '/internal_drive/Imported Data/Descriptors.xlsx',
    }
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__))
    
    # Step 2, reports reader pipeline:
    ReportsReaderPipeline.main(file_paths)



# Standalone execution:
if __name__ == '__main__':
    
    main()