import numpy as np
import os
import cv2
import pydicom
import math
import imageio
from collections import Counter
from PIL import Image
from scipy.spatial.distance import pdist, squareform
from scipy.signal import medfilt

def load_video(vid_dir, img_type='dicom', normalize=None, downsample=False, image_dim=(96*2,64*2), **kwargs):
    """
    Load all frames from video in a directory. Resize them and crop
    to a standard format. Normalize if necessary.

    Parameters
    ----------

    vid_dir : string
        Path to the directory containing the video.
    
    image_dim : tuple (optional)
        The (width, height) of the single frames.
        Default (96*2, 64*2) - cv2 convention

    normalize : string (optional) 
        'frame' - Normalize each frame by its mean and std.
        'video' - Normalize the entire video by its mean and std.
        
    downsample : bool (optional) 
        downsample frames, if true must set frames_per_vid param
        
    img_type : string (optional)
        One of ['dicom','jpg']

    Returns
    -------
     
    Echo_Frames : np.ndarray([nframes, width, height])
        A 3D array with the video.

    """

    Echo_Frames = []

    if img_type == 'jpg':
        # Walk through directory of jpegs and grab each frame
        frames = np.sort(os.listdir(vid_dir))
        indframes = [(int(frame.split('.')[0]), frame) for frame in frames if frame.split('.')[0] != '']
        indframes.sort(key = lambda x : x[0])
        frames = np.array([frame[1] for frame in indframes])
    
        for frame in frames:
            try:
                img = cv2.imread(vid_dir+'/'+frame, cv2.IMREAD_GRAYSCALE)
                Echo_Frames.append(img)
    
            except TypeError as te:
                if re.search('checkpoint', frame):
                    continue
                else:
                    raise te

    elif img_type == 'dicom':

        # Just load the video
        ds = pydicom.dcmread(vid_dir)
        for imi in range(ds.pixel_array.shape[0]):
            img = cv2.cvtColor(ds.pixel_array[imi], cv2.COLOR_RGB2GRAY)
            Echo_Frames.append(img)
    
    else:
        raise IOError('Type %s is not understood.' % img_type)

    Echo_Frames = np.array(Echo_Frames)
    
    if downsample:
        try:
            Echo_Frames = downsample_video(Echo_Frames, kwargs['frames_per_vid'], kwargs['ds_method'])
        except KeyError:
            Echo_Frames = downsample_video(Echo_Frames, kwargs['frames_per_vid'])

    # Resize if requested
    if image_dim is not None:
        efn = []
        for fi in range(Echo_Frames.shape[0]):
            img = cv2.resize(Echo_Frames[fi],image_dim)
            efn.append(img)
        Echo_Frames = np.array(efn)
                
    if normalize == 'frame':
        ntime = Echo_Frames.shape[0]
        means = Echo_Frames.reshape(ntime, -1).mean(-1)
        stds = Echo_Frames.reshape(ntime, -1).std(-1)
        
        Echo_Frames = Echo_Frames - means[:, np.newaxis, np.newaxis]
        Echo_Frames = Echo_Frames / stds[:, np.newaxis, np.newaxis]

    elif normalize == 'video':
        vid_mean = np.mean(Echo_Frames.ravel())
        vid_std = np.std(Echo_Frames.ravel())
        
        Echo_Frames = (Echo_Frames - vid_mean)/vid_std
        
    return Echo_Frames
    
def downsample_video(vid, frames_per_vid, method='mean'):
    delims = [math.floor(i*len(vid)/frames_per_vid) for i in list(range(1,frames_per_vid))]
    if method == 'mean':
        vid = np.array([np.mean(i, axis=0) for i in np.array_split(vid, delims)])
    elif method == 'first':
        vid = np.array([i[0] for i in np.array_split(vid, delims)])
    else:
        raise InputError("Method %s for downsampling not known."%method)
    
    return vid