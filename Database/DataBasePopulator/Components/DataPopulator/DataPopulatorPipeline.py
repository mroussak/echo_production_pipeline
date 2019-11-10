from Components.DataPopulator import DataPopulatorFunctions as funcs
import Tools.DatabaseTools as tools
import os



def main(file_paths):
    
    # unpack file paths:
    videos_table_file_path = file_paths['videos_table']
    manually_added_data_table_file_path = file_paths['manually_added_data_table']
    videos_query = file_paths['populate_videos']
    manually_added_data_table_query = file_paths['populate_manually_added_data']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__), **tools.kwargs)
    
    # Step 2, read tables:
    videos_table = tools.ReadDataFromFile(videos_table_file_path)
    manually_added_data_table = tools.ReadDataFromFile(manually_added_data_table_file_path)
    
    # Step 3, prep tables for entry:
    videos_table = funcs.PrepVideosTable(videos_table)
    manually_added_data_table = funcs.PrepManuallyAddedDataTable(manually_added_data_table)
    
    # Step 4, populate postgres:
    funcs.PopulateVideosTable(videos_table, videos_query)
    funcs.PopulateManuallyAddedDataTable(manually_added_data_table, manually_added_data_table_query)