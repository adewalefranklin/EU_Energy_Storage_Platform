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

--create clean customer master table from the raw layer

CREATE OR REPLACE TABLE customer_master_clean AS
SELECT
 "customer_id" AS CUSTOMER_ID,
    "customer_name" AS CUSTOMER_NAME,
    "contract_id" AS CONTRACT_ID,
    "facility_id" AS FACILITY_ID,
    TRY_TO_DOUBLE("capacity_mw") AS CAPACITY_MW,
    "contract_status" AS CONTRACT_STATUS,
    "credit_status" AS CREDIT_STATUS,
    TRY_TO_DOUBLE("credit_limit_eur") AS CREDIT_LIMIT_EUR,
    "risk_rating" AS RISK_RATING,
    TRY_TO_BOOLEAN("current_customer") AS CURRENT_CUSTOMER
FROM customer_master_raw;

SELECT *
FROM customer_master_clean
LIMIT 10;

--create clean facility master table from the raw layer

CREATE OR REPLACE TABLE facility_master_clean AS
SELECT
    "facility_id" AS FACILITY_ID,
    "country" AS COUNTRY,
    TRY_TO_DOUBLE("max_capacity_gwh") AS MAX_CAPACITY_GWH,
    "operator" AS OPERATOR,
    "maintenance_id" AS MAINTENANCE_ID,
    "maintenance_type" AS MAINTENANCE_TYPE,
    TO_DATE("scheduled_date") AS SCHEDULED_DATE,
    "event_id" AS EVENT_ID,
    TRY_TO_DOUBLE("imbalance_mwh") AS IMBALANCE_MWH,
    "severity" AS SEVERITY
FROM facility_master_raw;

SELECT *
FROM facility_master_clean
LIMIT 10;

--create clean sales operations table from the raw layer

CREATE OR REPLACE TABLE sales_operations_clean AS
SELECT
    "booking_id" AS BOOKING_ID,
    "customer_id" AS CUSTOMER_ID,
    TRY_TO_DOUBLE("booked_capacity_mw") AS BOOKED_CAPACITY_MW,
    TO_DATE("booking_date") AS BOOKING_DATE,
    "facility" AS FACILITY,
    COALESCE("nomination_id", '-') AS NOMINATION_ID,
    COALESCE("facility_id", "facility") AS FACILITY_ID,
    TRY_TO_DOUBLE("gas_volume_mwh") AS GAS_VOLUME_MWH,
    COALESCE("nomination_status", '-') AS NOMINATION_STATUS,
    TO_DATE("gas_price_date") AS GAS_PRICE_DATE,
    TRY_TO_DOUBLE("ttf_price_eur_mwh") AS TTF_PRICE_EUR_MWH,
    TRY_TO_DOUBLE("nbp_price_eur_mwh") AS NBP_PRICE_EUR_MWH
FROM sales_operations_raw;

SELECT* 
FROM SALES_OPERATIONS_CLEAN
LIMIT 5

