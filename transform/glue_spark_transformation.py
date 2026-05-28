# This is a sample AWS Glue job script that performs transformations on raw CSV data and writes the results to Parquet format in S3. It also demonstrates how to perform joins to create master tables for customers, facilities, sales operations, and contracts.

import sys

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "RAW_PATH",
        "OUTPUT_PATH",
    ],
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

raw_path = args["RAW_PATH"]
output_path = args["OUTPUT_PATH"]

"""
Silver transformation: customer information raw CSV to Parquet
"""

df_risk_mgt = spark.read.option("header", True).csv(
    raw_path
)  # Repeated for customer_info and risk_mgt files
df_risk_mgt.printSchema()
df_risk_mgt.show(5, truncate=False)

df_risk_mgt.write.mode("overwrite").parquet(output_path)


"""
Joins (creating customer master table) -- gold medallion layer for customers
"""

credit_df = spark.read.parquet("s3://eu-energy-platform/silver/credit_worthiness/")

contacts_df = spark.read.parquet("s3://eu-energy-platform/silver/customer_contacts/")

risk_df = spark.read.parquet("s3://eu-energy-platform/silver/risk_management/")

master_df = risk_df.join(credit_df, on="customer_id", how="left").join(
    contacts_df, on="customer_id", how="left"
)

master_df.write.mode("overwrite").parquet(
    "s3://eu-energy-platform/gold/customer_master_table/"
)

"""
Silver transformation: facility maintenance raw CSV to Parquet
"""

df_f_maintenance = spark.read.option("header", True).csv(raw_path)
df_f_maintenance.printSchema()
df_f_maintenance.show(5, truncate=False)
df_f_maintenance.write.mode("overwrite").parquet(output_path)

"""
Silver transformation: events raw CSV to Parquet
"""

df_events = spark.read.option("header", True).csv(raw_path)
df_events.printSchema()
df_events.show(5, truncate=False)
df_events.write.mode("overwrite").parquet(output_path)

"""
Silver transformation: storage facilities raw CSV to Parquet
"""
df_storage = spark.read.option("header", True).csv(raw_path)
df_storage.printSchema()
df_storage.show(5, truncate=False)
df_storage.write.mode("overwrite").parquet(output_path)

"""
Joins (creating facility master table) -- gold medallion layer for facilities
"""

storage_df = spark.read.parquet("s3://eu-energy-platform/silver/storage/")

maintenance_df = spark.read.parquet(
    "s3://eu-energy-platform/silver/facility_maintenance/"
)

events_df = spark.read.parquet("s3://eu-energy-platform/silver/events/")

facility_master_df = storage_df.join(maintenance_df, on="facility_id", how="left").join(
    events_df, on="facility_id", how="left"
)

facility_master_df.printSchema()
facility_master_df.show(10, truncate=False)

facility_master_df.write.mode("overwrite").parquet(
    "s3://eu-energy-platform/gold/facility_master_table/"
)

"""
Silver transformation: capacity bookings raw CSV to Parquet
"""
df_booked_capacity = spark.read.option("header", True).csv(raw_path)
df_booked_capacity.printSchema()
df_booked_capacity.show(5, truncate=False)
df_booked_capacity.write.mode("overwrite").parquet(output_path)

"""
Silver transformation: nominations raw CSV to Parquet
"""
df_nominations = spark.read.option("header", True).csv(raw_path)
df_nominations.printSchema()
df_nominations.show(5, truncate=False)
df_nominations.write.mode("overwrite").parquet(output_path)

"""
Silver transformation: gas prices raw CSV to Parquet
"""
df_gas_prices = spark.read.option("header", True).csv(raw_path)
df_gas_prices.printSchema()
df_gas_prices.show(5, truncate=False)
df_gas_prices.write.mode("overwrite").parquet(output_path)

"""
Joins (creating sales operations (master table) -- gold medallion layer for sales operations
"""

capacity_df = spark.read.parquet("s3://eu-energy-platform/silver/capacity_bookings/")

nominations_df = spark.read.parquet("s3://eu-energy-platform/silver/nominations/")

gas_prices_df = spark.read.parquet(
    "s3://eu-energy-platform/silver/gas_prices/"
).withColumnRenamed("booking_date", "gas_price_date")

c = capacity_df.alias("c")
n = nominations_df.alias("n")
g = gas_prices_df.alias("g")

sales_operations_df = c.join(
    n, F.col("c.facility") == F.col("n.facility_id"), "left"
).join(g, F.col("c.booking_date") == F.col("g.gas_price_date"), "left")

sales_operations_df.write.mode("overwrite").parquet(
    "s3://eu-energy-platform/gold/sales_operations_table/"
)

sales_operations_df.printSchema()
sales_operations_df.show(10, truncate=False)

"""
Silver transformation: contract capacity information raw CSV to Parquet
"""

df_contract_capacity = spark.read.option("header", True).csv(raw_path)
df_contract_capacity.printSchema()
df_contract_capacity.show(5, truncate=False)

df_contract_capacity.write.mode("overwrite").parquet(output_path)

"""
Silver transformation: contracts information raw CSV to Parquet
"""

df_contracts = spark.read.option("header", True).csv(raw_path)
df_contracts.printSchema()
df_contracts.show(5, truncate=False)

df_contracts.write.mode("overwrite").parquet(output_path)

"""
Joins (creating contracts (master table) -- gold medallion layer for booked capacity contracts
"""

contracts_df = spark.read.parquet("s3://eu-energy-platform/silver/contracts/")

contract_capacity_df = (
    spark.read.parquet("s3://eu-energy-platform/silver/contract_capacity/")
    .withColumnRenamed("end_date", "capacity_end_date")
    .withColumnRenamed("start_date", "capacity_start_date")
)

contract_master_df = contracts_df.join(
    contract_capacity_df, on="contract_id", how="left"
)

contract_master_df.write.mode("overwrite").parquet(
    "s3://eu-energy-platform/gold/contract_master_table/"
)

job.commit()