from Pipeline.Tools import Tools as tools
import subprocess
import numpy as np
import pickle
import cv2
import os



@tools.monitor_me()
def GetData(data_file_path):
    
    ''' Accepts data file path, returns object '''
    
    with open(data_file_path, 'rb') as handle:
        data = pickle.load(handle)
    
    return data
    
    
    
@tools.monitor_me()
def BuildMediaBaseDirectory(MEDIA_DIR):
    
    ''' Accepts file paths, builds media base '''
    
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    

    
@tools.monitor_me()
def BuildJpegs(dicom, destination):
    
    pass
    
    
    
@tools.monitor_me()
def BuildGif(dicom, destination):
    
    pass
    
    
    
@tools.monitor_me()
def BuildAVI(dicom, destination):
    
    ''' Accepts dicom, destination, builds avi file '''
    
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    FPS = 10
    seconds = dicom['number_of_frames'] / FPS
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(destination, fourcc, float(FPS), (width, height))
    
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    video.release()
    
    
    
@tools.monitor_me()
def BuildMP4(dicom, destination):
    
    ''' Accepts dicom, destination, builds mp4 file '''
    
    # get video data:
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    FPS = 1/dicom['seconds_per_frame']
    seconds = dicom['number_of_frames'] / FPS
    
    # create temporary destination for opencv:
    temp_destination = destination + '_temp_.mp4'
    
    # specify opencv, cv2 details:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(temp_destination, fourcc, float(FPS), (width, height))
    
    # compile video frame by frame:
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    # release video:
    video.release()
    
    # convert mp4 codec to web-uable coded:
    subprocess.run(['ffmpeg', '-loglevel', 'panic', '-i', temp_destination, '-vcodec', 'libx264', '-acodec', 'aac', destination])
    


@tools.monitor_me()
def BuildWebm(dicom, destination):
    
    ''' Accepts dicom, destination, builds webm file '''
    
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    FPS = 1/dicom['seconds_per_frame']
    seconds = dicom['number_of_frames'] / FPS
    
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    video = cv2.VideoWriter(destination, fourcc, float(FPS), (width, height))
    
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    video.release()
    
    
    
@tools.monitor_me()
def BuildWebmGrayscale(dicom, destination):
    
    # initialize variables:
    grayscale_frames = []
    
    # convert dicom data to grayscale:
    for frame in dicom['pixel_data']:
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        grayscale_frames.append(grayscale_frame)
    
    # convert to np array:
    grayscale_frames = np.array(grayscale_frames)
    
    width = grayscale_frames.shape[2]
    height = grayscale_frames.shape[1]
    FPS = 10
    seconds = dicom['number_of_frames'] / FPS
    
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    video = cv2.VideoWriter(destination, fourcc, float(FPS), (width, height))
    
    for frame in grayscale_frames:
        video.write(frame)
    
    video.release()