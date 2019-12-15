from Components.VideosTableReportsColumn import VideosTableReportsColumnPipeline
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
        'reports_table_export' : '/sandbox/dsokol/echo_production_pipeline/Database/Tables/reports_table.pkl',
        'populate_query' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/DataManagementQueries/populate_reports_table.sql',
        'insert_report_id_column_query' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/DataManagementQueries/insert_report_id_columns.sql',
    }
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__))
    
    # Step 2, reports reader pipeline:
    #ReportsReaderPipeline.main(file_paths)

    # Step 3, videos table reports column pipeline:
    VideosTableReportsColumnPipeline.main(file_paths)


# Standalone execution:
if __name__ == '__main__':
    
    main()