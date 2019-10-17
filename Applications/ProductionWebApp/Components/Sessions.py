import random
import string



def GetSessionID(request, verbose=False):
    
    session_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    if verbose:
        print('[GetSessionID] Found session id [%s]' %session_id)
    
    return session_id