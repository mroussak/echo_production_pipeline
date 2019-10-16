import os



def BuildRootDirectory(user_id, session_id, verbose=False):
    
    root_directory = '/internal_drive/Users/' + user_id + '/Sessions/' + session_id + '/'
    
    if verbose:
        print('[BuildRootDirectory]: Built root directory [%s]' %root_directory)
        
    return root_directory
    
    

def BuildDirectoryTree(root_directory, verbose=False):
    
    if not os.path.exists(root_directory):
    
        videos_directory = root_directory + 'Videos/'
        tables_directory = root_directory + 'Tables/'
        reports_directory = root_directory + 'Reports/'
        dicoms_directory = root_directory + 'Dicoms/'
        
        os.makedirs(videos_directory)
        os.makedirs(tables_directory)
        os.makedirs(reports_directory)
        os.makedirs(dicoms_directory)
    
    if verbose:
        print('[BuildDirectoryTree]: Built directory tree')