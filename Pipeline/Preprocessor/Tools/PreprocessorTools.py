from time import time



def ExportDicom(dicom, status, verbose=False, start=time()):
    
    ''' Accepts dicom, status, returns dicom ready for export '''
    
    export_dicom = {
        'dicom' : dicom,
        'status' : status,
    }
    
    if verbose:
        print('[@ %7.2f s] [ExportDicom]: Exported dicom object' %(time()-start))
    
    return export_dicom