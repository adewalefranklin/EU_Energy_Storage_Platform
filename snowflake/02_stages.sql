CREATE OR REPLACE STORAGE INTEGRATION s3_init
STORAGE_PROVIDER = 's3'
ENABLED = TRUE
TYPE = EXTERNAL_STAGE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::972775291781:role/snowflake-weather-role'
STORAGE_ALLOWED_LOCATIONS = (
's3://eu-energy-platform/gold/contract_master_table/',
's3://eu-energy-platform/gold/customer_master_table/',
's3://eu-energy-platform/gold/facility_master_table/',
's3://eu-energy-platform/gold/sales_operations_table/'
);
DESC INTEGRATION s3_init;


CREATE OR REPLACE STAGE contract_stage
URL = 's3://eu-energy-platform/gold/contract_master_table/'
STORAGE_INTEGRATION = s3_init
FILE_FORMAT = parquet_file;

CREATE OR REPLACE STAGE customer_stage
URL = 's3://eu-energy-platform/gold/customer_master_table/'
STORAGE_INTEGRATION = s3_init
FILE_FORMAT = parquet_file;

CREATE OR REPLACE STAGE facility_stage
URL = 's3://eu-energy-platform/gold/facility_master_table/'
STORAGE_INTEGRATION = s3_init
FILE_FORMAT = parquet_file;

CREATE OR REPLACE STAGE sales_operations_stage
URL = 's3://eu-energy-platform/gold/sales_operations_table/'
STORAGE_INTEGRATION = s3_init
FILE_FORMAT = parquet_file;

LIST @contract_stage;
LIST @customer_stage;
LIST @facility_stage;
LIST @sales_operations_stage;
