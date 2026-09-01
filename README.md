# Credit Risk ETL Pipeline & Analytics

An automated, end-to-end ETL pipeline built for credit risk analytics. This pipeline ingests daily loan data, cleanses and validates risk parameters, loads the processed data into Google Cloud Platform (GCP) BigQuery, and feeds updated metrics into Power BI dashboards.

---

## Architecture & Data Flow

```text
Local CSV / Source Data 
       │
       ▼
GitHub Actions Runner
  ├── 1. Extract & Simulate: Samples 50 daily incoming loan records
  ├── 2. Transform: Cleans text, handles null values, drops duplicates, validates business rules
  └── 3. Load: Backs up data locally & appends directly to GCP BigQuery
       │
       ▼
Google BigQuery Data Warehouse (`loan_portfolio.loan_clean`)
       │
       ▼
Power BI Executive Risk Dashboard
