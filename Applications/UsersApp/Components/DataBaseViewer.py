from Models import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Functions import ValidateUser
import sqlite3 as sq
import pandas as pd
import datetime



def InsertRow():
    
    ''' Adds new user to user table '''
    
    try:
        # connect:
        engine = create_engine('sqlite:///webapp.db', echo=True)
    
        # open session:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # add new row:
        user = User('daniel@icardio.ai','hellohi123')
        session.add(user)
        
    except Exception as error:
        print('[ERROR] in [InsertRow]: [%s]' %error)
        
    finally:    
        session.commit()
    
    
    
    
def QueryDatabase():
    
    ''' Queries database, returns results '''
    
    query = 'select * from users;'
    #query = 'SELECT name FROM sqlite_master WHERE type ="table" AND name NOT LIKE "sqlite_%";'
    
    try:
        # connect:
        connection = sq.connect("webapp.db")
        cursor = connection.cursor()
        
        # query:
        result = cursor.execute(query).fetchall()
        
    except Exception as error:
        print('[ERROR] in [QueryDatabase]: [%s]' %error)
        return None
    
    finally:
        return result
        
        

# Main:
if __name__ == '__main__':
    
    # Step 1, add entry to database:
    #InsertRow()
    
    # Step 2, query database:
    result = QueryDatabase()
    #result = ValidateUser('daniel@icardio.ai','hellohi123')
    
    # Step 3, export result:
    print('Result: [%s]' %result)