from time import time
import os



# Accepts file path, deletes all files in file path:
def DeleteFilesInPath(file_path, verbose=False, start=time()):
    
    file_list = os.listdir(file_path)
    
    for file in file_list:
        os.remove(file_path + file)
    
    if verbose:
        print('[@ %7.2f s] [DeleteFilesInPath]: cleared  [%s]' %(time()-start, file_path))
