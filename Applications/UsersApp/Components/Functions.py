from .Models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlite3 as sq
import pandas as pd
import datetime
import random
import string


### User Login Validation ###
def ValidateUser(email, password, verbose=False):
    
    ''' Accepts email, password, verifies if crednetials are correct '''
    
    try:
        # connect:
        engine = create_engine('sqlite:///webapp.db', echo=False)
    
        # open session:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # query for email:
        query = session.query(User).filter(User.email.in_([email]))
        result = query.first()
        
        # email does not exist:
        if result == None:
            
            if verbose:
                print('[ValidateUser]: Incorrect email [%s]' %email)
            
            return {'code' : 0, 'message' : 'incorrect email', 'result' : result}
            
        # query for password:
        query = session.query(User).filter(User.email.in_([email]), User.password.in_([password]))
        result = query.first()
        
        # password incorrect:
        if result == None:
            
            if verbose:
                print('[ValidateUser]: Incorrect password')
            
            return {'code' : 1, 'message' : 'incorrect password', 'result' : result}
            
    except Exception as error:
        errorStr = '[ERROR] in [ValidateUser]: [%s]' %error
        print(errorStr)
        return {'code': -1, 'message': errorStr, 'result': None}
        
    else:
        if verbose:
            print('[ValidateUser]: Validated [%s]' %email)
        
        return {'code' : 2, 'message' : 'user validated', 'result' : result}
    
    finally:    
        session.commit()
        
        
### User Registration and Email Validation ###
def RegisterUser(email, password, name, tel, verbose=False):
    
    ''' Accepts email, password, verifies if crednetials are correct '''
    
    try:
        # connect:
        engine = create_engine('sqlite:///webapp.db', echo=False)
    
        # open session:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # query for email:
        query = session.query(User).filter(User.email.in_([email]))
        result = query.first()
        
        # email does not exist - it's an new user:
        if result != None:
            return {'code' : 0, 'message' : 'Email already in use.'}
            
        # add user to database:
        new_user = User(email, password, name, tel)
        result = session.add(new_user)
        query = session.query(User).filter(User.email.in_([email]))
        result = query.first()
        print('-------((((((((((((((', result)
        # Registration done
        return {'code' : 2, 'message' : 'Success', 'result' : result}
            
    except Exception as error:
        print('[ERROR] in [RegisterUser]: [%s]' %error)
        return {'code': 0, 'message': str(error)}
        
    else:
        if verbose:
            print('[RegisterUser]: Validated [%s]' %email)
        
        return {'code' : 2, 'message' : 'user validated', 'result' : result}
    
    finally:    
        session.commit()

        

def GetUserID(request, verbose=False):
    
    user_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    if verbose:
        print('[GetUserID] Found user id [%s]' %user_id)
    
    return user_id
    

    
def GetSessionID(request, verbose=False):
    
    session_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    if verbose:
        print('[GetSessionID] Found session id [%s]' %session_id)
    
    return session_id