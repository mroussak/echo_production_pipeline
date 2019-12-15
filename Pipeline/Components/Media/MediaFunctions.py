from Tools import Tools as tools
import pickle
import cv2
import os



@tools.monitor()
def GetDicomData(dicom_data_file_path):
    
    ''' Accepts dicom data file path, returns dicom object '''
    
    with open(dicom_data_file_path, 'rb') as handle:
        dicom = pickle.load(handle)
    
    return dicom
    
    
    
@tools.monitor()
def BuildMediaBaseDirectory(MEDIA_DIR):
    
    ''' Accepts file paths, builds media base '''
    
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    

    
@tools.monitor()
def BuildJpegs(dicom, destinaton):
    
    pass
    
    
    
@tools.monitor()
def BuildGif(dicom, destinaton):
    
    pass
    
    
    
@tools.monitor()
def BuildAVI(dicom, destinaton):
    
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    FPS = 10
    seconds = dicom['number_of_frames'] / FPS
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(destinaton, fourcc, float(FPS), (width, height))
    
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    video.release()
    
    
    
@tools.monitor()
def BuildMP4(dicom, destinaton):
    
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    FPS = 10
    seconds = dicom['number_of_frames'] / FPS
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #fourcc = cv2.VideoWriter_fourcc(*'H264')
    #fourcc = 0x00000021
    video = cv2.VideoWriter(destinaton, fourcc, float(FPS), (width, height))
    
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    video.release()
    


@tools.monitor()
def BuildWebm(dicom, destinaton):
    
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    FPS = 10
    seconds = dicom['number_of_frames'] / FPS
    
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    video = cv2.VideoWriter(destinaton, fourcc, float(FPS), (width, height))
    
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    video.release()