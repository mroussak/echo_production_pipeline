SELECT 
    object_id,  
    TRIM(path_to_dicom_webm) AS path_to_dicom_webm
FROM 
    ManuallyAddedViewsData
WHERE 
    view is NULL 
AND 
    in_use = false
LIMIT 1;