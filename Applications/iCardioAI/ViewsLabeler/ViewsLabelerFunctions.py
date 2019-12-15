from datetime import datetime, timedelta
from time import time



def ParseLabels(request, verbose=False, start=time()):
    
    ''' Accepts request object, returns parsed labels '''
    
    # object id:
    object_id = request.POST.get("object_id", "")
    
    # view, subview:
    view = request.POST.get("view", "")
    subview = request.POST.get("subview", "")
    
    # quality:
    quality = request.POST.get("image_quality", "")
    
    # user id:
    user_id = request.POST.get("user_id", "")
    
    # selection time:
    selection_time = request.POST.get("selection_time", "")
    
    # time stamp:
    time_stamp = datetime.now()
    
    # previous object id:
    previous_object_id = request.session['previous_object_id']
    
    # get labels:
    labels = {
        'object_id' : object_id,
        'view' : view,
        'subview' : subview,
        'quality' : quality,
        # 'quality1' : request.POST.get("quality1", ""), 
        # 'quality2' : request.POST.get("quality2", ""),
        # 'quality3' : request.POST.get("quality3", ""),
        # 'quality4' : request.POST.get("quality4", ""),
        # 'quality5' : request.POST.get("quality5", ""),
        'user_id' : user_id,
        'selection_time' : selection_time,
        'time_stamp' : time_stamp,
        'previous_object_id' : previous_object_id,
        }
    
    if verbose:
        print('[ParseLabels]: Parsed labels from request object:')
    
    return labels