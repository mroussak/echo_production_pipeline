from Pipeline.Tools import Tools as tools
import subprocess
import numpy as np
import pickle
import ffmpeg
import cv2
import os



@tools.monitor_me()
def GetData(data_file_path):
    
    ''' Accepts data file path, returns object '''
    
    # initialize variables:
    data = None
    
    # check if file exists:
    if os.path.exists(data_file_path):
    
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
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(destination, fourcc, float(FPS), (width, height))
    
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    video.release()
    
    

# @tools.monitor_me()
# def BuildMP4(dicom, destination):
    
#     ''' Accepts dicom, destination, builds mp4 file '''
    
#     # exit if dicom does not exist:
#     if dicom is None:
#         return
    
#     # get video data:
#     width = dicom['pixel_data'].shape[2]
#     height = dicom['pixel_data'].shape[1]
#     framerate = 1/dicom['seconds_per_frame']
    
#     # create ffmpeg process:
#     process = (
#         ffmpeg
#             .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
#             .output(destination, pix_fmt='yuv420p', vcodec='libx264', r=framerate)
#             .overwrite_output()
#             .run_async(pipe_stdin=True)
#     )
    
#     # iterate over each frame:
#     for frame in dicom['pixel_data']:
#         process.stdin.write(
#             frame
#                 .astype(np.uint8)
#                 .tobytes()
#         )
#     process.stdin.close()
#     process.wait()
    
    
    
@tools.monitor_me()
def BuildMP4(dicom, destination):
    
    ''' Accepts dicom, destination, builds mp4 file '''
    
    # exit if dicom does not exist:
    if dicom is None:
        return
    
    # get video data:
    width = dicom['pixel_data'].shape[2]
    height = dicom['pixel_data'].shape[1]
    framerate = 1/dicom['seconds_per_frame']
    
    # create temporary destination for opencv:
    temp_destination = destination + '_temp_.mp4'
    
    # specify opencv, cv2 details:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(temp_destination, fourcc, float(framerate), (width, height))
    
    # compile video frame by frame:
    for frame in dicom['pixel_data']:
        video.write(frame)
    
    # release video:
    video.release()
    
    # convert mp4 codec to web-usable coded:
    subprocess.run(['ffmpeg', '-loglevel', 'panic', '-y', '-i', temp_destination, '-vcodec', 'libx264', '-acodec', 'aac', destination])
    


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
    