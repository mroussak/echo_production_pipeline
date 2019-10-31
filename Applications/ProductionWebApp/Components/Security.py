from time import time



# Accepts list of files, returns message, status:
def CheckForDicoms(files, verbose=False, start=time()):

    # no files are submitted:
    if len(files) == 0:
        message = 'No files submitted'
        status = -1
        return message, status

    # file other than dicom submitted:
    for file in files:
        if file.filename[-3:] != 'dcm':
            message = '[%s] is not a dicom' %(file.filename)
            status = -2
            return message, status
    
    # file list okay:
    message = 'Reading dicoms'
    status = 1

    if verbose:
        print('[@ %7.2f s] [CheckForDicoms]: Verified file list' %(time()-start))

    return message, status
