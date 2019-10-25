import Components.PostgresCallerFunctions as funcs
from time import time



# Main:
def main(query_type, verbose=False, start=time()):
    
    # Variables:
    kwargs = { 
        'verbose' : True, 
        'start' : time(),
    }
    file_paths = {
        'select_query' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/select_query.psql',
        'create_table_query' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/create_table_query.psql',
        #'select_query' : r'/internal_drive/echo_production_pipeline/Database/EchoData/Queries/insert_query.psql',
        'insert_query' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/select_query.psql',
        #'insert_query' : r'/internal_drive/echo_production_pipeline/Database/EchoData/Queries/insert_query.psql',
    }
    database_dictionary = {
        'host' : 'localhost',
        'database' : 'datavalidation',
        'user' : 'icardio',
        'password' : 'hellohi123',
    }
    
    # Step 1, read query:
    database_query = funcs.ReadDatabaseQuery(file_paths[query_type], **kwargs)

    # Step 2, query database:
    result = funcs.QueryDatabase(database_dictionary, database_query, **kwargs)
    
    # Step 3, export results:
    return result
    
    
    
if __name__ == '__main__':
    
    query_type = 'create_table_query'
    
    main(query_type, verbose=True, start=time())