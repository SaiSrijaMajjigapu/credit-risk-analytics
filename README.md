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
```
## Tech Stack & Tools
* Data Processing: Python 3.10, Pandas, pandas-gbq

* Cloud & Storage: Google Cloud Platform (GCP), BigQuery

* Orchestration & CI/CD: GitHub Actions

* Security & IAM: GCP Service Accounts, Encrypted GitHub Secrets

Reporting: Power BI
## Automation & Workflow
Managed via .github/workflows/etl_workflow.yml:

* Scheduled Runs: Automated daily execution at 00:00 UTC via Cron (0 0 * * *).

* Manual Trigger: Supports on-demand execution via workflow_dispatch in the GitHub interface.

* Authentication: Passes encrypted GCP credentials (GCP_SA_KEY) safely to the runner environment at execution time.
## Power BI Dashboard
The Power BI dashboard provides an overview of the loan portfolio, credit risk, loan performance, and key financial KPIs.

<table>
  <tr>
    <td><img src="screenshots/Screenshot(635).png" width="100%"></td>
    <td><img src="screenshots/screenshot(636).png" width="100%"></td>
  </tr>
  <tr>
    <td><img src="screenshots/screenshot(637).png" width="100%"></td>
    <td><img src="screenshots/screenshot(638).png" width="100%"></td>
  </tr>
</table>
## Key Skills Demonstrated
* Data Processing & ETL: Python, Pandas, Data Cleaning & Validation

* Cloud Storage: Google Cloud BigQuery

* Automation: GitHub Actions (Scheduled Daily Runs)

* Data Visualization: Power BI, Interactive Dashboards
## Repository Structure
```text
credit-risk-analytics/
├── .github/
│   └── workflows/
│       └── etl_workflow.yml   # Automation setup
├── data/
│   └── credit_risk_analytics.csv   # Input dataset
├── .gitignore                 # Files excluded from GitHub
├── README.md
└── etl.py                     # Primary Python script
```
