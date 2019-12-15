from Components.WebmCompiler import WebmCompilerFunctions as funcs
import Tools.DatabaseTools as tools
import os



def main(file_paths):
    
    # unpack file paths:
    videos_table_file_path = file_paths['videos_table']
    manually_added_data_table_file_path = file_paths['manually_added_data_table']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), **tools.kwargs)
    
    # Step 2, read vidoes table:
    videos_table = tools.ReadDataFromFile(videos_table_file_path)

    # Step 3, create manually added data table:
    manually_added_data_table = funcs.BuildManuallyAddedDataTable(videos_table)
    
    # Step 4, build webms:
    funcs.BuildWebmFiles(manually_added_data_table)
    
    # Step 5, export data:
    tools.ExportDataToFile(manually_added_data_table, manually_added_data_table_file_path)