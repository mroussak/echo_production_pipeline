from Configuration.Configuration import kwargs
import Tools.DatabaseTools as tools
import pandas as pd
import hashlib
import sys

# Database imports:
#sys.path.insert(1, '/internal_drive/echo_production_pipeline/Database/EchoData/')
sys.path.insert(1, '/sandbox/dsokol/echo_production_pipeline/Database/EchoData/')
import PostgresCaller



@tools.time_it(**kwargs)
def ParseReports(reports):
    
    ''' Accepts reports, returns parsed reports '''
    
    reports = reports.rename(columns={'Pulm Artery' : 'Pulmonary Artery'})
    
    return reports
    
    

@tools.time_it(**kwargs)
def ReadDescriptors(descriptors_file):
    
    ''' Accepts descriptors file path, returns descriptors as dataframe '''
    
    # initialize variables:
    descriptors = {}
    
    partitions = [
        'Left Ventricle', 'Left Atrium',
        'Right Ventricle', 'Right Atrium', 'Aortic Valve', 'Mitral Valve',
        'Pulmonic Valve', 'Tricuspid Valve', 'Aortic Root', 'Aortic Arch',
        'Pericardium', 'Pulmonary Artery'
    ]
    
    for partition in partitions: 
        
        # create descriptor object:
        descriptor = {partition : pd.read_excel(descriptors_file, partition)} 
        
        # append to descriptors:
        descriptors.update(descriptor)

    return descriptors
    
    

@tools.time_it(**kwargs)
def GetDictionaryOfNormalDescriptors(descriptors):

    ''' Accepts descriptors, returns dictionary of normal descriptors '''
    
    # intialize variables:
    normal_features = {}

    # get list of features of heart:
    features = list(descriptors.keys())

    # iterate over each feature:
    for feature in features:

        # get dataframe of descriptors for given feature:
        feature_descriptors = descriptors[feature]

        # get list of descritors for 'normals':
        normals = feature_descriptors.loc[feature_descriptors['Abnormal'] == 0]
        normal_feature_descriptors = list(normals[feature])

        # create normal_feature object:
        normal_feature_object = {
            feature : normal_feature_descriptors, 
        }

        # add to dictonary:
        normal_features.update(normal_feature_object)

    return normal_features
    
    
    
@tools.time_it(**kwargs)
def BuildReportTable(normal_features, reports, descriptors):

    ''' Accepts normal features dictionary, raw reports dataframe, descriptors, returns reports table '''
    
    # get list of features of heart:
    features = list(descriptors.keys())   

    # add binary columns to reports:
    for feature in features:
    
        # get list of normal descriptors:
        list_of_normal_features = normal_features[feature]
    
        # check if descriptor is in list of normal descriptors:
        reports[feature + '_binary'] = reports[feature].apply(lambda descriptor: 0 if (descriptor in list_of_normal_features) else 1)
    
    # get list of binary columns:
    columns = list(reports.columns)
    binary_columns = [descriptor for descriptor in columns if '_binary' in descriptor] 
    
    # get subset of reports table:
    binary_reports_table = reports[binary_columns]
    
    # add abnormality column:
    reports['abnormality'] = binary_reports_table.sum(axis=1)
    
    # create unique id:
    reports['object_id'] = reports['Report Dir'].map(str) + reports['Patient'].map(str) + reports['Date'].map(str)
    reports['object_id'] = reports['object_id'].map(lambda x: x.encode('utf-8'))
    reports['object_id'] = reports['object_id'].map(lambda x: hashlib.sha224(x).hexdigest())

    # rename columns:
    reports = reports.rename(columns={
        'Report Dir'      : 'reports_directory', 'Patient'         : 'visit_guid',      'Date'             : 'visit_date', 
        'Left Ventricle'  : 'left_ventricle',    'Left Atrium'     : 'left_atrium',     'Right Ventricle'  : 'right_ventricle',
        'Right Atrium'    : 'right_atrium',      'Aortic Valve'    : 'aortic_valve',    'Mitral Valve'     : 'mitral_valve',
        'Pulmonic Valve'  : 'pulmonic_valve',    'Tricuspid Valve' : 'tricuspid_valve', 'Aortic Root'      : 'aortic_root', 
        'Aortic Arch'     : 'aortic_arch',       'Pericardium'     : 'pericardium',     'Pulmonary Artery' : 'pulmonary_artery', 
        'EF'              : 'ejection_fraction', 
        'Left Ventricle_binary'  : 'left_ventricle_binary',  'Left Atrium_binary'      : 'left_atrium_binary', 
        'Right Ventricle_binary' : 'right_ventricle_binary', 'Right Atrium_binary'     : 'right_atrium_binary',
        'Aortic Valve_binary'    : 'aortic_valve_binary',    'Mitral Valve_binary'     : 'mitral_valve_binary', 
        'Pulmonic Valve_binary'  : 'pulmonic_valve_binary',  'Tricuspid Valve_binary'  : 'tricuspid_valve_binary',
        'Aortic Root_binary'     : 'aortic_root_binary',     'Aortic Arch_binary'      : 'aortic_arch_binary',
        'Pericardium_binary'     : 'pericardium_binary',     'Pulmonary Artery_binary' : 'pulmonary_artery_binary',
    })
        
    # name dataframe:
    reports.name = 'reports_table'
        
    return reports
    


@tools.time_it(**kwargs)
def ExportReportsTable(reports_table, query):

    ''' Accepts reports table, writes to database '''
    
    reports_table = reports_table.to_dict(orient='records')
    
    for parameters in reports_table:
        
        try:
            PostgresCaller.main(query, parameters)
        
        except:
            pass
    