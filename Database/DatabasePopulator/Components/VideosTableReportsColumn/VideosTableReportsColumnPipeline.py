import Components.VideosTableReportsColumn.VideosTableReportsColumnFunctions as funcs
from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
import os



def main(file_paths):
    
    # Unpack files:
    insert_report_id_column_query = file_paths['insert_report_id_column_query']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__))
    
    # Step 2, find report ids for each video:
    ids_table = funcs.FindReportIDs()
    
    # Step 3, add report id column to videos table:
    funcs.AddReportIDsToVidoes(ids_table, insert_report_id_column_query)