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



def view_postprocessing(seg_dictionary):
    unique_views = ['A2C', 'A3C', 'A4C', 'A5C', 'PLAX', 'PSAX', 
                    'PSAXA', 'RVIT', 'SUBA', 'SUBB', 'SUPA']
    dicom_id = seg_dictionary['dicom_id']
    max_probs = []
    view_pred = []
    for frame_prob in seg_dictionary['predictions']:
        max_probs.append(max(frame_prob))
        view_pred.append(unique_views[np.where(frame_prob==max(frame_prob))[0][0]])
    most_common_view = Counter(view_pred).most_common(1)[0][0]
    most_common_view_prob = Counter(view_pred).most_common(1)[0][1]/len(view_pred)
    video_view_threshold = most_common_view_prob
    predicted_view = most_common_view
    probs_winning_class = np.array(max_probs)[np.where(np.array(view_pred) == most_common_view)[0]]
    frame_view_threshold = np.std(probs_winning_class)/np.mean(probs_winning_class)
    if (video_view_threshold>0.5) & (frame_view_threshold<0.1):
        usable_view=True
    else:
        usable_view=False
    result = {
        'dicom_id' : dicom_id,
        'predicted_view' : predicted_view, 
        'frame_view_threshold' : frame_view_threshold, 
        'video_view_threshold' : video_view_threshold,
        'usable_view' : usable_view,
    }
        
    return result



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



def psax_cylinder(mask, **kwargs):
    try:
        x_scale,y_scale = kwargs['x_scale'],kwargs['y_scale']
    except:
        x_scale, y_scale = 1, 1
    #Find axis of rotation using largest distance between two points
    mask = cv2.Canny(mask, 100, 200)
    y, x = np.nonzero(mask)
    pts = list(zip(*(x,y)))
    D = pdist(pts)
    D = squareform(D)
    N, [I_row, I_col] = np.nanmax(D), np.unravel_index(np.argmax(D), D.shape)
    min_coords = pts[I_row]
    max_coords = pts[I_col]
    height = math.sqrt((x_scale*(max_coords[0]-min_coords[0]))**2+(y_scale*(max_coords[1]-min_coords[1]))**2)
    pix_height = math.sqrt((max_coords[0]-min_coords[0])**2+(max_coords[1]-min_coords[1])**2)
#     min_max_line = cv2.line(img, max_coords, min_coords, 150, 2)
    x_v1 = np.subtract(max_coords,min_coords)[0]
    y_v1 = np.subtract(max_coords,min_coords)[1]
    theta = np.arctan((x_v1)/(y_v1))  
    rotation_mat = np.matrix([[np.cos(theta), -np.sin(theta)], 
                              [np.sin(theta), np.cos(theta)]])    
    #Define coordinates of lv and min max points
    coords_min_max = np.vstack([[max_coords[0], min_coords[0]], [max_coords[1], min_coords[1]]])
    coords_lv = np.vstack([x,y])
    #Find coordinates of lv in rotated image
    trns_coords_lv = rotation_mat*coords_lv
    x_trns_coords_lv, y_trns_coords_lv = trns_coords_lv.A        
    #Find coordinates of min/max points in rotated image
    trns_coords_min_max  = rotation_mat*coords_min_max
    x_coords_min_max , y_coords_min_max  = trns_coords_min_max.A
    
    #Find midpoint of ellipse
    mid_point_y_trns = sum(y_coords_min_max)/2    
    mid_point_x_trns = (min(x_trns_coords_lv)+max(x_trns_coords_lv))/2
#     mid_pt_lv_trns = np.array([[mid_point_x_trns], [mid_point_y_trns]])
#     mid_pt_lv = (np.transpose(rotation_mat)*mid_pt_lv_trns).A
    
    #Find points used to calculate width in original image
    trns_coords_for_width = np.vstack([[min(x_trns_coords_lv),max(x_trns_coords_lv)],
                                       [mid_point_y_trns,mid_point_y_trns]])
    pts_for_width = (np.transpose(rotation_mat)*trns_coords_for_width).A
    width_x = pts_for_width[0]
    width_y = pts_for_width[1]
    width = math.sqrt((x_scale*(width_x[0]-width_x[1]))**2+(y_scale*(width_y[0]-width_y[1]))**2)
    pix_width = math.sqrt(((width_x[0]-width_x[1])**2)+((width_y[0]-width_y[1])**2))

    t = np.linspace(0, 2*math.pi, 20)
    ellipse_x_pts_trns = mid_point_x_trns + (pix_width/2)*np.cos(t)
    ellipse_y_pts_trns = mid_point_y_trns + (pix_height/2)*np.sin(t)
    coords_ellipse_trns = np.vstack([ellipse_x_pts_trns, ellipse_y_pts_trns])
    coords_ellipse = np.transpose(rotation_mat)*coords_ellipse_trns
    coords_ellipse_x = coords_ellipse.A[0]
    coords_ellipse_y = coords_ellipse.A[1]
    return(height, width, np.vstack([coords_ellipse_x, coords_ellipse_y]))

def axis_of_symmetry(coords):
    cov = np.cov(coords)
    evals, evecs = np.linalg.eig(cov)
    sort_indices = np.argsort(evals)
    x_v1, y_v1 = evecs[:, sort_indices[0]]  # Eigenvector with largest eigenvalue
    x_v2, y_v2 = evecs[:, sort_indices[1]]
    theta = -np.arctan((y_v1)/(x_v1))  
    rotation_mat = np.matrix([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta), np.cos(theta)]])
    return(rotation_mat)    

def euclidean_distance(x,y):
    euc_dist = math.sqrt((x[1]-x[0])**2+(y[1]-y[0])**2)
    return(euc_dist)

def apical_disks(mask, number_of_disks):
    coords = []
    y, x = np.nonzero(mask) 
    mean_x, mean_y = np.mean(x), np.mean(y)
    x, y = x - mean_x, y - mean_y                                
    rotation_mat = axis_of_symmetry(np.vstack([x, y]))
    transformed_mat = rotation_mat*np.vstack([x, y])
    x_transformed, y_transformed = transformed_mat.A
    ##Find top and bottom extremities using axis of symmetry
    max_y, min_y = max(y_transformed[np.where((x_transformed-0)<1)]), min(y_transformed[np.where((x_transformed-0)<1)]) 
    top_bottom_extremities = np.transpose(rotation_mat)*[[0,0],[min_y,max_y]]
    x_extremities, y_extremities = top_bottom_extremities.A[0]+mean_x, top_bottom_extremities.A[1]+mean_y
    coord_0, coord_1 = (int(x_extremities[0]), int(y_extremities[0])), (int(x_extremities[1]), int(y_extremities[1]))
    coords.append([coord_0,coord_1])
    # Find left and right extremities for all disks
    top_bottom_distance = max_y-min_y
    if top_bottom_distance>20:
        number_of_disks = number_of_disks
        disk_length = top_bottom_distance/number_of_disks
        for disk_num in range(1,number_of_disks+1):
            right_x = max(x_transformed[np.where(abs(y_transformed-(min_y+(disk_num)*disk_length))<1)])
            left_x = min(x_transformed[np.where(abs(y_transformed-(min_y+(disk_num)*disk_length))<1)])
            right_y =  y_transformed[np.where(x_transformed==right_x)]
            left_y =  y_transformed[np.where(x_transformed==left_x)]  
            left_right_extremities = np.transpose(rotation_mat)*[[left_x,right_x],[left_y,right_y]]
            x_extremities, y_extremities = left_right_extremities.A[0]+mean_x, left_right_extremities.A[1]+mean_y
            coord_0, coord_1 = (int(x_extremities[0]), int(y_extremities[0])), (int(x_extremities[1]), int(y_extremities[1]))
            coords.append([coord_0, coord_1])
        return(coords)
    else:
        #raise Exception('length less than 20')
        pass
        
        
        
def seg_postprocessing_apical(seg_dictionary):
    dicom_id = seg_dictionary['dicom_id']
    thresh = 0.5
    original_vid = load_video(seg_dictionary['path_to_dicom_jpeg'], normalize='False', img_type='jpg', image_dim=None)
    original_img_size = original_vid.shape[1:]
    lv_diam = []
    lvv_simpson = []
    gif_pred_mask = []
    gif_simpson_disks = []
    number_of_disks = 20
    for idx, pred in enumerate(seg_dictionary['mask']):
        frame = original_vid[idx].astype(np.uint8)
        disk_volume = 0
        mask = np.where(pred[:,:,0]>thresh,255.0,0.0).astype(np.uint8)
        if (mask==0.0).all():
            im = Image.fromarray(frame)
            im.save(seg_dictionary['path_to_mask_jpeg']+'/'+str(idx)+'.jpg')
            gif_pred_mask.append(frame)
            gif_simpson_disks.append(frame)
            lv_diam.append(np.nan)                
            lvv_simpson.append(np.nan)
        else:   
    #         Using connected components
            ret, labels = cv2.connectedComponents(mask)
            (values,counts) = np.unique(labels,return_counts=True)
            values = values[1:]
            counts = counts[1:]
            ind=np.argmax(counts)
            mask = np.where(labels==values[ind],255.0,0.0)
            mask = cv2.resize(mask, original_vid.shape[1:][::-1])
            mask = np.where(mask==0.0,0.0,255.0).astype(np.uint8)
            overlayed_mask = cv2.addWeighted(frame,1,mask,0.5,0)   
            im = Image.fromarray(overlayed_mask)
            im.save(seg_dictionary['path_to_mask_jpeg']+'/'+str(idx)+'.jpg')
            gif_pred_mask.append(overlayed_mask)
            frame_for_simpsons = frame.copy()
            try:
                coords = apical_disks(mask, number_of_disks=number_of_disks)
                top_bottom_distance = math.sqrt(((1*(coords[0][1][0]-coords[0][0][0]))**2)+
                                                ((1*(coords[0][1][1]-coords[0][0][1]))**2)) 
                disk_length = top_bottom_distance/number_of_disks
                lv_diams = []
                for coord in coords:
                    cv2.line(frame_for_simpsons,tuple(coord[0]),tuple(coord[1]),100,1) 
                for coord in coords[1:]:
                    diam = math.sqrt(((seg_dictionary['len_x_pix']*(coord[1][0]-coord[0][0]))**2)+
                                                ((seg_dictionary['len_y_pix']*(coord[1][1]-coord[0][1]))**2)) 
                    lv_diams.append(diam)
                    disk_volume += np.pi*((diam/2)**2)*disk_length*seg_dictionary['len_y_pix']
                lv_diam.append(max(lv_diams))                
                lvv_simpson.append(disk_volume)
            except Exception as e:
                #print(e)
                lv_diam.append(np.nan)                
                lvv_simpson.append(np.nan)
            im = Image.fromarray(frame_for_simpsons)
            im.save(seg_dictionary['path_to_simpsons_jpeg']+'/'+str(idx)+'.jpg')
            gif_simpson_disks.append(frame_for_simpsons)
    lvv_simpson = medfilt(lvv_simpson)
    lvdd = max(lv_diam)
    lvsd = min(lv_diam)
    lvdv = max(lvv_simpson)
    lvsv = min(lvv_simpson)
    ef = (1-lvsv/lvdv)*100
    imageio.mimsave(seg_dictionary['path_to_mask_gif']+'/'+dicom_id+'.gif', gif_pred_mask)
    imageio.mimsave(seg_dictionary['path_to_simpsons_gif']+'/'+dicom_id+'.gif', gif_simpson_disks)
    return {'dicom_id' : dicom_id,'lvv_simpson' : lvv_simpson,'lvdd' : lvdd,'lvsd' : lvsd,'lvdv' : lvdv, 'lvsv' : lvsv, 'ef' : ef}
                    
## rename jpegs in order to properly sort them
def rename_jpegs(path):
    for root, dirs, files in os.walk(path):
        jpegs = [file for file in files if file.split('.')[-1]=='jpg']
        if len(jpegs)>100:
            for jpg in jpegs:
                if len(jpg.split('.')[0])==1:
                    os.rename(root+'/'+jpg, root+'/'+'00'+jpg)
                if len(jpg.split('.')[0])==2:
                    os.rename(root+'/'+jpg, root+'/'+'0'+jpg)   
        elif len(jpegs)>10:
            for jpg in jpegs:
                if len(jpg.split('.')[0])==1:
                    os.rename(root+'/'+jpg, root+'/'+'0'+jpg) 
        else:
            pass
        
        
def seg_postprocessing_psax(seg_dictionary):
    dicom_id = seg_dictionary['dicom_id']
    thresh = 0.5
    original_vid = load_video(seg_dictionary['path_to_dicom_jpeg'], normalize='False', img_type='jpg', image_dim=None)
    original_img_size = original_vid.shape[1:]
    lv_diam = []
    lvv_teichholz = []
    lvv_prolate_e = []
    gif_pred_mask = []
    gif_cylinder = []
    for idx, pred in enumerate(seg_dictionary['mask']):
        frame = original_vid[idx].astype(np.uint8)
        mask = np.where(pred[:,:,0]>thresh,255.0,0.0).astype(np.uint8)
        if (mask==0.0).all():
            im = Image.fromarray(frame)
            im.save(seg_dictionary['path_to_mask_jpeg']+'/'+str(idx)+'.jpg')
            gif_pred_mask.append(frame)
            gif_cylinder.append(frame)
            lv_diam.append(np.nan)                
            lvv_teichholz.append(np.nan)
            lvv_prolate_e.append(np.nan)
        else:   
    #         Using connected components
            ret, labels = cv2.connectedComponents(mask)
            (values,counts) = np.unique(labels,return_counts=True)
            values = values[1:]
            counts = counts[1:]
            ind=np.argmax(counts)
            mask = np.where(labels==values[ind],255.0,0.0)   
            mask = cv2.resize(mask, original_vid.shape[1:][::-1])
            mask = np.where(mask==0.0,0.0,255.0).astype(np.uint8)
            overlayed_mask = cv2.addWeighted(frame,1,mask,0.5,0)   
            im = Image.fromarray(overlayed_mask)
            im.save(seg_dictionary['path_to_mask_jpeg']+'/'+str(idx)+'.jpg')
            gif_pred_mask.append(overlayed_mask)
            original_img_rgb = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
            try:
                cylinder_info = psax_cylinder(mask,x_scale=seg_dictionary['len_x_pix'],y_scale=seg_dictionary['len_y_pix'])
                height = cylinder_info[0]
                width = cylinder_info[1]
                coords_ellipse_x = cylinder_info[2][0]
                coords_ellipse_y = cylinder_info[2][1]
                D1 = height
                D2 = width
                for i in range(len(coords_ellipse_x)):                     
                    original_img_rgb[int(coords_ellipse_y[i])-3:int(coords_ellipse_y[i])+3,int(coords_ellipse_x[i])-3:int(coords_ellipse_x[i])+3] = [0,0,255]                
                lv_diam.append(D1)
                lvv_teichholz.append((7/(2.4+D1))*(D1**3))
                lvv_prolate_e.append((math.pi/3)*(D1**2)*D2)
            except Exception as e:
                print(e)
                lv_diam.append(np.nan)
                lvv_teichholz.append(np.nan)
                lvv_prolate_e.append(np.nan)                
            im = Image.fromarray(original_img_rgb)
            im.save(seg_dictionary['path_to_cylinder_jpeg']+'/'+str(idx)+'.jpg')
            gif_cylinder.append(original_img_rgb)
            
    lvv_teichholz = medfilt(lvv_teichholz)
    lvv_prolate_e = medfilt(lvv_prolate_e)
    
    lvsv_teichholz = min(lvv_teichholz)    
    lvdv_teichholz = max(lvv_teichholz)
    
    lvsv_prolate_e = min(lvv_prolate_e)    
    lvdv_prolate_e = max(lvv_prolate_e)
    
    ef_teichholz = (1-lvsv_teichholz/lvdv_teichholz)*100
    ef_prolate_e = (1-lvsv_prolate_e/lvdv_prolate_e)*100
    
    imageio.mimsave(seg_dictionary['path_to_mask_gif']+'/'+'pred_mask.gif', gif_pred_mask)
    imageio.mimsave(seg_dictionary['path_to_cylinder_gif']+'/'+'cylinder.gif', gif_cylinder)

    return {'dicom_id' : dicom_id,'lvv_teichholz' : lvv_teichholz, 'lvv_prolate_e' : lvv_prolate_e, 'lvsv_teichholz' : lvsv_teichholz, 'lvdv_teichholz' : lvdv_teichholz, 'lvsv_prolate_e' : lvsv_prolate_e, 'lvdv_prolate_e' : lvdv_prolate_e, 'ef_teichholz' : ef_teichholz , 'ef_prolate_e' : ef_prolate_e}