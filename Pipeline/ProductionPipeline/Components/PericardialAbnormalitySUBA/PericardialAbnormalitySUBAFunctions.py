import Components.Models.ModelsPipeline as models
import Tools.ProductionTools as tools
from billiard import Pool
#from multiprocessing import Pool
from time import time
import pandas as pd
import numpy as np
import os



def ParseViewsData(views_data, view, videos_directory, verbose=False, start=time()):
    
    ''' Accepts views data, returns parsed views data '''

    # sort for relevant data:
    views_data = views_data.loc[views_data['predicted_view'] == view]
    
    # take two best views:
    views_data = views_data.sort_values(by=['video_view_threshold'], ascending=False)
    views_data = views_data.iloc[:2]

    # name dataframe:
    views_data.name = view + '_views_data'
    
    if verbose:
        print("[@ %7.2f s] [ParseViewsData]: Parsed views_data" %(time()-start))
        
    return views_data
    
    
    

def PredictPericardialAbnormality(suba_views_data, verbose, start):
    
    pass



def ProcessPericardialAbnormalityResults(suba_predictions, verbose, start):
    
    pass