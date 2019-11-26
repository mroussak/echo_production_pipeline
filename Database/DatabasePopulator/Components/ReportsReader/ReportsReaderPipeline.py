import Components.ReportsReader.ReportsReaderFunctions as funcs
from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
import os



# Main:
def main(file_paths):
    
    # Unpack files:
    reports_table = file_paths['reports_table']
    descriptors_file = file_paths['descriptors']
    export_file = file_paths['reports_table_export']
    populate_query = file_paths['populate_query']
    
    # Step 1, initialize script:
    tools.InitializeScript(os.path.basename(__file__))
    
    # Step 2, read reports files:
    reports = tools.ReadDataFromFile(reports_table)
    
    # Step 3, parse reports:
    reports = funcs.ParseReports(reports)
    
    # Step 4, read descriptors:
    descriptors = funcs.ReadDescriptors(descriptors_file)
    
    # Step 5, get dictionary of normal descriptors:
    normal_features = funcs.GetDictionaryOfNormalDescriptors(descriptors)
    
    # Step 6, build reports table:
    reports_table = funcs.BuildReportTable(normal_features, reports, descriptors)
    
    # Step 7, write reports table to database:
    tools.ExportDataToFile(reports_table, export_file)
    funcs.ExportReportsTable(reports_table, populate_query)
    
    return reports, descriptors, reports_table