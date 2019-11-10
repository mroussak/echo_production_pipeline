CREATE TABLE FactTable(
    object_id TEXT PRIMARY KEY,
    manually_added_views_data_id TEXT REFERENCES ManuallyAddedViewsData(object_id)
);