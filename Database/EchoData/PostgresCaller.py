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
        'create_table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/create_table_query.psql',
        'alter_table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/alter_table_query.psql',
        'select' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/select_query.psql',
        'insert' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/insert_query.psql',
        'update' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/update_query.psql',
        'clean' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/clean_query.psql',
        'table' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/table_query.psql',
        'delete' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/delete_table_query.psql',
        'populate' : r'/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/populate_query.psql',
        #'select' : r'/internal_drive/echo_production_pipeline/Database/EchoData/Queries/select_query.psql',
        #'insert' : r'/internal_drive/echo_production_pipeline/Database/EchoData/Queries/insert_query.psql',
    }
    
    web_app_queries = {
        'SELECT_get_next_unlabeled_view' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/SELECT_get_next_unlabeled_view.psql',
        'SELECT_get_previous_view' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/SELECT_get_previous_view.psql',
        'UPDATE_add_previous_object_id' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_add_previous_object_id.psql',
        'UPDATE_add_view_label_to_row' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_add_view_label_to_row.psql',
        'UPDATE_set_view_to_in_use' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_set_view_to_in_use.psql',
        'UPDATE_set_view_to_not_in_use' : '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/Queries/UPDATE_set_view_to_not_in_use.psql',
    }

    query_file = file_paths['create_table']
    #query_file = file_paths['alter_table']
    query_file = file_paths['select']
    #query_file = file_paths['insert']
    #query_file = file_paths['update']
    #query_file = file_paths['clean']
    #query_file = file_paths['table']
    #query_file = file_paths['delete']
    #query_file = file_paths['populate']
    
    #query_file = web_app_queries['SELECT_get_next_unlabeled_view']
    #query_file = web_app_queries['UPDATE_add_previous_object_id']
    #query_file = web_app_queries['UPDATE_add_view_label_to_row']
    #query_file = web_app_queries['UPDATE_set_view_to_in_use']
    #query_file = web_app_queries['UPDATE_set_view_to_not_in_use']
    
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
    
        print(result)
    except:
        pass