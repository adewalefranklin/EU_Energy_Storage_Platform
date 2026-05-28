--create clean contract master table from the raw layer

CREATE OR REPLACE TABLE contract_master_clean AS
SELECT
    "contract_id" AS contract_id,
    TO_DATE("start_date") AS start_date,
    TO_DATE("end_date") AS end_date,
    TRY_TO_DOUBLE("price_eur_per_mwh") AS price_eur_per_mwh
FROM contract_master_raw;

SELECT*
FROM contract_master_clean
LIMIT 5;