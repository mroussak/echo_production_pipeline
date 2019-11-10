import Components.PostgresCallerFunctions as funcs
from datetime import datetime, timedelta
from time import time



# Main:
def main(query_file, parameters, verbose=False, start=time()):
    
    # Variables:
    database_dictionary = {
        'host' : 'userbase.c23mx66autdz.us-west-2.rds.amazonaws.com',
        'port' : 5432,
        'database' : 'postgres',
        'user' : 'icardio',
        'password' : 'Hellohi123!',
    }
    kwargs = {
        'verbose' : verbose,
        'start' : start,
    }
    
    # Step 1, read raw query:
    database_query = funcs.ReadDatabaseQuery(query_file, parameters, **kwargs)

    # Step 2, query database:
    result = funcs.QueryDatabase(database_dictionary, database_query, **kwargs)
    
    # Step 3, export results:
    return result
    
    
    
if __name__ == '__main__':

    file_paths = {
        'create_table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/create_table_query.sql',
        #'create_table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/create_fact_table_query.sql',
        'alter_table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/alter_table_query.psql',
        'select' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/select_query.sql',
        'insert' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/insert_query.sql',
        'update' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/update_query.sql',
        'clean' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/clean_query.sql',
        'table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/table_query.sql',
        'delete' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/delete_table_query.sql',
        'populate' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/populate_query.sql',
        'schema' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/GeneralQueries/select_schema_query.sql',
        #'select' : r'/internal_drive/echo_production_pipeline/Database/EchoData/Queries/select_query.psql',
        #'insert' : r'/internal_drive/echo_production_pipeline/Database/EchoData/Queries/insert_query.psql',
    }

    #query_file = file_paths['create_table']
    #query_file = file_paths['schema']
    #query_file = file_paths['alter_table']
    query_file = file_paths['select']
    #query_file = file_paths['insert']
    #query_file = file_paths['update']
    #query_file = file_paths['clean']
    #query_file = file_paths['table']
    #query_file = file_paths['delete']
    #query_file = file_paths['populate']
    
    parameters = {
        'object_id' : 1,
        'view' : None,
        'subview' : None,
        'quality' : None,
        'user_id' : None,
        'selection_time' : None,
        'time_stamp' : None,
        'previous_object_id' : None,
    }
    # parameters = {
    #     'previous_object_id' : 0,
    #     'object_id' : 1,
    # }
    
    result = main(query_file, parameters, verbose=True, start=time())
    print(result)
    
    try:
        result_strings = result.select_dtypes(['object'])
        result[result_strings.columns] = result_strings.apply(lambda x: x.str.strip())
    
        print(result.iloc[0])    
    except:
        pass