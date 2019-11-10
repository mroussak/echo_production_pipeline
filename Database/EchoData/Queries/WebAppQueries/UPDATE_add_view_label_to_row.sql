UPDATE 
    ManuallyAddedViewsData
SET 
    view = TRIM('{view}'),
    subview = TRIM('{subview}'),
    user_id = TRIM('{user_id}'),
    selection_time = TRIM('{selection_time}'),
    time_stamp = '{time_stamp}'::TIMESTAMP,
    previous_object_id = '{previous_object_id}',
    quality = '{quality}'
WHERE 
    object_id = '{object_id}';
