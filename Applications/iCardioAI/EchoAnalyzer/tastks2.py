#import what you need

 ModelsPipeline.main(verbose=True, start=time())
 
 while True:
     
     
     sql = 'SELECT * FROM echoanalyzer_visits where start_processing_at is null order by created asc LIMIT 1'
     
     #do query in db
     
     #if there is a row of data
    
    
    
    sql_files = 'SELECT file FROM echoanlyzer_files WHERE visit_id = %d' % row['id']
    
    file_list = ....
     
    root_directory = tools.BuildRootDirectory(row['username'], str(row['id']))
    tools.BuildDirectoryTree(root_directory)
    ProductionPipeline.main(row['username'], str((row['id']), s3_files=file_list, verbose=verbose, start=time(), views_model=ret[0], graph=ret[1])
    
    time.sleep(15)