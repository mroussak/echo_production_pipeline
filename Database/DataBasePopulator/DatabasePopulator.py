from Components.WebmCompiler import WebmCompilerPipeline
from Components.DataParser import DataParserPipeline
from Components.DataPopulator import DataPopulatorPipeline



# Main:
if __name__ == '__main__':

    # File structure:
    file_paths = {
        'videos_table' : '/sandbox/dsokol/echo_production_pipeline/Database/Tables/videos_table.pkl',
        'manually_added_data_table' : '/sandbox/dsokol/echo_production_pipeline/Database/Tables/manually_added_data_table.pkl',
        'populate_videos' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/DataManagementQueries/populate_videos_table.sql',
        'populate_manually_added_data' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/DataManagementQueries/populate_manually_added_data_table.sql',
        }

    # Step 1, DataParserPipeline:
    #DataParserPipeline.main(file_paths)
    
    # Step 2, WebmCompilerPipeline:
    #WebmCompilerPipeline.main(file_paths)
    
    # Step 3, DataPopulatorPipeline:
    DataPopulatorPipeline.main(file_paths)