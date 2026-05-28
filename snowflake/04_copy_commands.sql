--copy data from raw layer in to the raw contract master table

COPY INTO contract_master_raw
FROM @contract_stage
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT *
FROM contract_master_raw
LIMIT 10;