# EU Energy Storage Platform

An enterprise-style cloud data engineering platform that simulates real-world energy storage operations, customer risk management, sales operations, and contract management workflows using AWS, Spark, Snowflake, and medallion architecture principles.

## Project Overview

This project was designed to simulate how a modern energy company could centralize fragmented operational and commercial data into a scalable cloud-based lakehouse platform.

The platform ingests structured and unstructured datasets from multiple simulated business departments including:

* Risk Management
* Sales Operations
* Facilities Management
* Contract Management

The project implements a medallion architecture approach:

```text
Raw Layer   → source ingestion
Silver Layer → cleaned standardized parquet datasets
Gold Layer  → business-ready master tables
```

---

# Architecture

## Technologies Used

* AWS S3
* AWS Glue
* PySpark
* Snowflake
* Parquet
* Python
* Medallion Architecture

---

# Data Domains

## Risk Management Domain

Datasets:

* credit_worthiness
* customer_contacts
* risk_management

Gold Output:

* customer_master_table

Business Goal:
Create a unified customer risk and exposure view.

---

## Facilities Domain

Datasets:

* storage
* facility_maintenance
* events

Gold Output:

* facility_master_table

Business Goal:
Create a facility operational and maintenance overview.

---

## Sales Operations Domain

Datasets:

* capacity_bookings
* nominations
* gas_prices

Gold Output:

* sales_operations_table

Business Goal:
Combine booked capacity, operational nominations, and market gas pricing into a unified operational analytics layer.

---

## Contract Management Domain

Datasets:

* contracts
* contract_capacity

Gold Output:

* contract_master_table

Business Goal:
Create a centralized contract and capacity allocation master dataset.

---

# S3 Lakehouse Structure

```text
s3://eu-energy-platform/

raw/
silver/
gold/
```

---

# Current Gold Tables

```text
gold/
├── customer_master_table/
├── facility_master_table/
├── contract_master_table/
└── sales_operations_table/
```

---

# Current Features

* Multi-domain enterprise data modelling
* Raw → Silver → Gold medallion architecture
* Spark transformations with AWS Glue
* Parquet standardization
* Business-oriented master table creation
* Realistic enterprise join scenarios
* Handling of inconsistent business keys and column names
* Structured and unstructured data preparation
* Snowflake external stage integration
* Snowflake raw and clean layer modelling
* Schema inference using Snowflake INFER_SCHEMA
* Automated Parquet ingestion using COPY INTO
* dbt staging layer implementation
* Dimensional modelling (Dimensions & Facts)
* Business mart creation
* SCD Type 2 historical tracking using dbt Snapshots
* Data quality testing with dbt Tests
* Data lineage and documentation with dbt Docs
* Analytics schema separation (RAW → ANALYTICS)
* GitHub Actions CI pipeline
* Pytest-based unit testing with mocking
* Config-driven pipeline architecture
* Centralized logging and exception handling

---

# Snowflake Data Warehouse Layer

Implemented Components:

* External stages connected to AWS S3
* Storage integration using IAM role-based access
* Parquet file ingestion
* Raw layer modelling
* Clean layer modelling
* Schema inference with INFER_SCHEMA
* COPY INTO ingestion pipelines
* Analytics schema separation
* Snapshot schema for historical tracking

Current Snowflake Architecture:

```text
AWS S3 (Gold Layer)
        ↓
Snowflake Stage
        ↓
RAW Tables
        ↓
CLEAN Tables
        ↓
ANALYTICS Schema
        ↓
SNAPSHOTS Schema
```

---

# dbt Integration

Implemented Components:

* dbt project initialization
* Snowflake profile configuration
* Analytics schema integration
* Staging layer models
* Dimension models
* Fact models
* Business marts
* Data quality tests
* Data lineage generation
* Documentation generation
* SCD Type 2 snapshots

Current Models:

```text
ANALYTICS

STAGING
├── STG_CONTRACT_MASTER
├── STG_CUSTOMER_MASTER
├── STG_FACILITY_MASTER
└── STG_SALES_OPERATIONS

DIMENSIONS
├── DIM_CONTRACT
├── DIM_CUSTOMER
└── DIM_FACILITY

FACTS
└── FACT_SALES_OPERATIONS

MARTS
├── CUSTOMER_RISK
├── FACILITY_UTILIZATION
└── CONTRACT_ANALYTICS
```

Current Snapshots:

```text
SNAPSHOTS
└── SNAP_CUSTOMER_MASTER
```

Business Goal:

Create reusable, tested, documented, and historically traceable analytical models for downstream reporting, risk management, and business intelligence.

---

# Current Data Platform Architecture

```text
API / Departmental Data Sources
                ↓
AWS S3 Raw Layer
                ↓
AWS Glue (PySpark)
                ↓
AWS S3 Gold Layer
                ↓
Snowflake Stage
                ↓
RAW Tables
                ↓
CLEAN Tables
                ↓
dbt Staging Models
                ↓
Dimensions & Facts
                ↓
Business Marts
                ↓
Snapshots (SCD2)
                ↓
Power BI
```

---

# CI/CD

Implemented Components:

* GitHub Actions workflow
* Automated pytest execution
* Dependency validation
* dbt project validation

---

# Future Enhancements

## Airflow Orchestration

* End-to-end workflow scheduling
* Monitoring and retries
* Automated Snowflake loading orchestration

## PDF Processing Pipeline

Future support for:

* AWS Textract
* Contract metadata extraction
* Document intelligence workflows

## Power BI Dashboards

Planned analytical dashboards for:

* Customer risk exposure
* Facility operations
* Commercial sales operations
* Contract analytics
* Storage utilization analytics

## Advanced CI/CD

Future support for:

* Automated dbt deployment pipelines
* Snowflake environment promotion
* Infrastructure validation
* Production release automation

## Data Governance

Future support for:

* Role-Based Access Control (RBAC)
* Data masking policies
* Row-level security
* Data catalog integration
