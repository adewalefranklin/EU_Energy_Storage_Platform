--copy data from raw layer in to the raw contract master table

COPY INTO contract_master_raw
FROM @contract_stage
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT *
FROM contract_master_raw
LIMIT 10;

--copy data from raw layer in to the raw customer master table

COPY INTO customer_master_raw
FROM @customer_stage
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT *
FROM customer_master_raw
LIMIT 10;

--copy data from raw layer in to the raw facility master table

COPY INTO facility_master_raw
FROM @facility_stage
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT *
FROM facility_master_raw
LIMIT 10;

--copy data from raw layer in to the raw sales operations table

COPY INTO sales_operations_raw
FROM @sales_operations_stage
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
