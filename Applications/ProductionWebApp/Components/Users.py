import random
import string



def GetUserID(request, verbose=False):
    
    user_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    if verbose:
        print('[GetUserID] Found user id [%s]' %user_id)
    
    return user_id