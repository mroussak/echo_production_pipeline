CREATE TABLE ViewsVisibilityMatrix(
    subview TEXT,
    left_ventricle TEXT,
    left_atrium TEXT,
    right_ventricle TEXT,
    right_atrium TEXT,
    aortic_valve TEXT,
    mitral_valve TEXT,
    pulmonic_valve TEXT,
    tricuspid_valve TEXT,
    aortic_root TEXT,
    aortic_arch TEXT,
    pericardium TEXT,
    pulmonary_artery TEXT
);

-- CREATE TABLE Reports(
--     object_id TEXT PRIMARY KEY,
--     reports_directory TEXT,
--     visit_guid TEXT,
--     visit_date TEXT,
--     left_ventricle TEXT,
--     left_atrium TEXT,
--     right_ventricle TEXT,
--     right_atrium TEXT,
--     aortic_valve TEXT,
--     mitral_valve TEXT,
--     pulmonic_valve TEXT,
--     tricuspid_valve TEXT,
--     aortic_root TEXT,
--     aortic_arch TEXT,
--     pericardium TEXT,
--     pulmonary_artery TEXT,
--     ejection_fraction FLOAT,
--     left_ventricle_binary INT,
--     left_atrium_binary INT,
--     right_ventricle_binary INT,
--     right_atrium_binary INT,
--     aortic_valve_binary INT,
--     mitral_valve_binary INT,
--     pulmonic_valve_binary INT,
--     tricuspid_valve_binary INT,
--     aortic_root_binary INT,
--     aortic_arch_binary INT,
--     pericardium_binary INT,
--     pulmonary_artery_binary INT,
--     abnormality INT
-- );

-- CREATE TABLE ManuallyAddedViewsData(
--     object_id TEXT PRIMARY KEY,
--     video_id TEXT,
--     previous_object_id TEXT,
--     path_to_dicom_webm TEXT,
--     in_use BOOLEAN DEFAULT false,
--     view TEXT,
--     subview TEXT,
--     quality TEXT,
--     user_id TEXT,
--     selection_time TEXT,
--     time_stamp TIMESTAMPTZ
-- );

-- CREATE TABLE Videos(
--     object_id TEXT PRIMARY KEY,
--     path_to_jpegs TEXT,
--     patient_hash TEXT,
--     visit_date TEXT,
--     folder TEXT
-- );