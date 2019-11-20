from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
import pandas as pd



@tools.time_it(**kwargs)
def ReadDescriptors(descriptors_file):
    
    ''' Accepts descriptors file path, returns descriptors as dataframe '''
    
    # initialize variables:
    descriptors = {}
    
    partitions = [
        'Left Ventricle', 'Left Atrium',
        'Right Ventricle', 'Right Atrium', 'Aortic Valve', 'Mitral Valve',
        'Pulmonic Valve', 'Tricuspid Valve', 'Aortic Root', 'Aortic Arch',
        'Pericardium', 'Pulminary Artery'
    ]
    
    for partition in partitions: 
        
        # create descriptor object:
        descriptor = {partition : pd.read_excel(descriptors_file, partition)} 
        
        # append to descriptors:
        descriptors.update(descriptor)

    return descriptors        
    