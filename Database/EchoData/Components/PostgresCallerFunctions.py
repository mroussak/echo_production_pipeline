from configparser import ConfigParser
import Tools.DatabaseTools as tools
import pandas.io.sql as sqlio
from time import time
import pandas as pd
import psycopg2



def ReadDatabaseQuery(query, parameters=None, verbose=False, start=time()):
        
    ''' Accepts query file, returns database query '''    
    
    # read query from file:
    if query[0] == '/':
        
        # read query from file:
        with open(query, 'r') as file:
            database_query = file.read()
            
        # add key words to query:
        if parameters:
            database_query = database_query.format(**parameters)
    
    # ready query from string:
    else:
        database_query = query
        
    if verbose:
        print('[@ %7.2f s] [ReadDatabaseQuery]: Read database query from [%s]' %(time()-start, query))
    
    return database_query



def QueryDatabase(database_dictionary, database_query, verbose=False, start=time()):
    
    ''' Accepts database dictionary, SQL query string, returns query results '''
    
    # intialize variables:
    result = None
    
    try:
        
        # establish connection:
        connection = psycopg2.connect(
            host = database_dictionary['host'],
            database = database_dictionary['database'],
            user = database_dictionary['user'],
            password = database_dictionary['password'],
        )

        # build cursor:
        cursor = connection.cursor()

        # execute query:
        cursor.execute(database_query)
    
        # retreive result (select queries only):
        if tools.QueryType(database_query) == 'SELECT':
            result = sqlio.read_sql_query(database_query, connection)

        # commit changes:
        connection.commit()
        
        # close cursor:
        cursor.close()
        
    except Exception as error:
        
        # handle exceptions:
        raise('[ERROR] in [QueryDatabase] with query [%s]: Database error: %s' %(database_query, error))

    finally:
        
        # close connection:
        if connection is not None:
            connection.close()
    
    if verbose:
        print('[@ %7.2f s] [QueryDatabase]: Queried database' %(time()-start))
        
    return result