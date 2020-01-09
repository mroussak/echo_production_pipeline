from Pipeline.Components.Reports import ReportsFunctions as funcs



def ReportsPipeline(file_paths):
    
    # unpack file paths:
    dicom_data = file_paths['dicom_data']
    view_data = file_paths['view_data']
    segmentation_data = file_paths['segmentation_data']
    report_destination = file_paths['reports_json']
    
    print('\n[ReportsPipeline]__')
    
    # Step 1, get data:
    dicom_data = funcs.GetData(dicom_data)
    view_data = funcs.GetData(view_data)
    segmentation_data = funcs.GetData(segmentation_data)
    
    # Step 2, build json:
    report_json = funcs.BuildReportJson(file_paths, dicom_data, view_data, segmentation_data)
    
    # Step 3, export json:
    funcs.ExportReportJson(report_json, report_destination)