CREATE TABLE ManuallyAddedViewsData(
    object_id TEXT PRIMARY KEY,
    video_id TEXT,
    previous_object_id TEXT,
    path_to_dicom_webm TEXT,
    in_use BOOLEAN DEFAULT false,
    view TEXT,
    subview TEXT,
    quality TEXT,
    user_id TEXT,
    selection_time TEXT,
    time_stamp TIMESTAMPTZ
);

-- CREATE TABLE Videos(
--     object_id TEXT PRIMARY KEY,
--     path_to_jpegs TEXT,
--     patient_hash TEXT,
--     visit_date TEXT,
--     folder TEXT
-- );