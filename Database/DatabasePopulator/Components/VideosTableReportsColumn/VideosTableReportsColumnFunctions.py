from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
import pandas as pd
import hashlib
import sys

# Database imports:
#sys.path.insert(1, '/internal_drive/echo_production_pipeline/Database/EchoData/')
sys.path.insert(1, '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/')
import PostgresCaller



@tools.time_it(**kwargs)
def FindReportIDs():
    
    ''' Queries database for reports and videos, returns joined data '''
    
    # build queries:
    reports_query = 'SELECT * FROM reports;'
    videos_query = 'SELECT * from videos;'
    
    # query database:
    reports = PostgresCaller.main(reports_query)
    videos = PostgresCaller.main(videos_query)
    
    # join data:
    reports = reports.rename(columns={'object_id' : 'report_id'})
    videos = videos.rename(columns={'object_id' : 'video_id', 'patient_hash' : 'visit_guid'})
    videos = videos.drop(['report_id'], axis=1)
    result = reports.merge(videos)
    
    # drop unused columns:
    result = result[['report_id', 'video_id']]
    result = result.rename(columns={'video_id' : 'object_id'})
    
    return result
    
    
    
@tools.time_it(**kwargs)
def AddReportIDsToVidoes(ids_table, insert_report_id_column_query):
    
    ''' Accepts ids dataframe, adds report ids to videos table '''
    
    ids_table = ids_table.to_dict(orient='records')
    
    for parameters in ids_table:
        
        PostgresCaller.main(insert_report_id_column_query, parameters)
    
        