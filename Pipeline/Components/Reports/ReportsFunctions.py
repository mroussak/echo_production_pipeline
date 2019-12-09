from Tools import Tools as tools
import pickle
import json



@tools.monitor()
def GetData(data_file_path):
    
    ''' Accepts dicom data file path, returns dicom object '''
    
    with open(data_file_path, 'rb') as handle:
        dicom = pickle.load(handle)
    
    return dicom
    


@tools.monitor()
def BuildReportJson(file_paths, dicom_data, view_data):
    
    report_json = {
        'user_id' : file_paths['user_id'],
        'visit_id' : file_paths['visit_id'],
        'dicom_id' : file_paths['dicom_id'],
        'view' : {
            'dicom_id' : view_data['dicom_id'],
            'predicted_view' : view_data['predicted_view'], 
            'frame_view_threshold' : view_data['frame_view_threshold'], 
            'video_view_threshold' : view_data['video_view_threshold'],
            'usable_view' :view_data['usable_view'],
        },
        'dicom' : {
            'dicom_id' : dicom_data['dicom_id'],
            'manufacturer' : dicom_data['manufacturer'],
            'manufacturer_model_name' : dicom_data['manufacturer_model_name'],
            'physical_units_x_direction' : dicom_data['physical_units_x_direction'],
            'physical_units_y_direction' : dicom_data['physical_units_y_direction'],
            'physical_delta_x' : dicom_data['physical_delta_x'],
            'physical_delta_y' : dicom_data['physical_delta_y'],
            'dicom_type' : dicom_data['dicom_type'],
            'number_of_frames' : dicom_data['number_of_frames'],
        },
        'media' : {
            'mp4' : file_paths['dicom_mp4'],
        },
        'reports' : {
            'log' : file_paths['log_file'],
        }
    }
    
    return report_json
    
    

@tools.monitor()
def ExportReportJson(report_json, report_destination):
    
    with open(report_destination, 'w') as json_file:
        json.dump(report_json, json_file)