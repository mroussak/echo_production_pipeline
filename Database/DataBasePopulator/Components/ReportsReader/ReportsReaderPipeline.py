import Components.ReportsReader.ReportsReaderFunctions as funcs
from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
import os



# Main:
def main(file_paths):
    
    # Unpack files:
    reports_table = file_paths['reports_table']
    descriptors_file = file_paths['descriptors']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__))
    
    # Step 2, read reports files:
    reports = tools.ReadDataFromFile(reports_table)
    
    # Step 3, read descriptors:
    descriptors = funcs.ReadDescriptors(descriptors_file)
    
    print(descriptors.keys())
    
    