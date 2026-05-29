-- This SQL script is designed to create raw tables in Snowflake by inferring the schema from Parquet files stored in specified stages. The script uses the `INFER_SCHEMA` function to automatically read the schema of the Parquet files and dynamically create the table structure without manually defining columns. This approach allows for more flexibility in handling evolving schemas.
 
 ------------------------------------------------------------
 ------------------------------------------------------------

-- inspect contract_stage and create raw table

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

--inspect customer_stage and create raw table

SELECT *
FROM TABLE(
    INFER_SCHEMA(
     LOCATION => '@customer_stage',
     FILE_FORMAT => 'parquet_file'
    )
)
;

CREATE OR REPLACE TABLE customer_master_raw
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@customer_stage',
            FILE_FORMAT => 'parquet_file'
        )
    )
);


-- inspect facilty stage and create raw table

SELECT*
FROM TABLE(
   INFER_SCHEMA(
    LOCATION => '@facility_stage',
    FILE_FORMAT => 'parquet_file'
   )
);

--create raw facility master table

CREATE OR REPLACE TABLE facility_master_raw
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@facility_stage',
            FILE_FORMAT => 'parquet_file'
        )
    )
);


-- inspect sales operations stage and create raw table

SELECT*
FROM TABLE(
   INFER_SCHEMA(
   LOCATION => '@sales_operations_stage',
   FILE_FORMAT => 'parquet_file'
   )
);

--create raw and clean sales operations tables

CREATE OR REPLACE TABLE sales_operations_raw
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@sales_operations_stage',
            FILE_FORMAT => 'parquet_file'
        )
    )
);


