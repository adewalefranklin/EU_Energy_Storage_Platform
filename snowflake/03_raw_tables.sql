SELECT *
FROM TABLE(
    INFER_SCHEMA(
        LOCATION => '@contract_stage',
        FILE_FORMAT => 'parquet_file'
    )
);

--This method of cotract_master_raw table creation below does the following:

-- Read the Parquet schema automatically
-- Dynamically create the table structure
-- Avoid manually defining columns
-- Handle evolving schemas more flexibly

CREATE OR REPLACE TABLE contract_master_raw
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@contract_stage',
            FILE_FORMAT => 'parquet_file'
        )
    )
);

