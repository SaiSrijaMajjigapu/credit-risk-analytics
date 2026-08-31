import os
import pandas as pd
import pandas_gbq


# Extract & Simulate Step
def extract_data(file_path, num_records=50):
    """
    Extract data from source CSV and simulate incoming daily records.
    """
    try:
        source_df = pd.read_csv(file_path)
        print(f"Source loaded successfully: {source_df.shape[0]} rows.")

        # Sample records to simulate incoming batch
        df = source_df.sample(n=min(num_records, len(source_df))).copy()
        print(f"Simulated batch created: {df.shape[0]} incoming rows.")
        return df

    except Exception as e:
        print(f"Error loading source data: {e}")
        return None


# Transform Step
def transform_data(df):
    """
    Clean text formatting, fill missing values, deduplicate, and validate business logic.
    """
    try:
        df_clean = df.copy()

        # Clean text columns
        text_cols = df_clean.select_dtypes(include=["object"]).columns
        for col in text_cols:
            df_clean[col] = df_clean[col].fillna("not_provided").astype(str).str.strip()

        # Fill missing numeric values
        num_cols = df_clean.select_dtypes(include=["number"]).columns
        for col in num_cols:
            df_clean[col] = df_clean[col].fillna(0)

        # Deduplicate records
        rows_before = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        print(f"Duplicate records removed: {rows_before - len(df_clean)}")

        # Validate business logic
        if "loan_amount" in df_clean.columns:
            df_clean = df_clean[df_clean["loan_amount"] > 0]

        if "annual_income" in df_clean.columns:
            df_clean = df_clean[df_clean["annual_income"] > 0]

        print(f"Data transformed successfully: {df_clean.shape[0]} valid rows.")
        return df_clean

    except Exception as e:
        print(f"Error transforming data: {e}")
        return None


# Load Step
def load_data(df, output_path, project_id, dataset_table):
    """
    Save local backup CSV and append batch to BigQuery.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)

        pandas_gbq.to_gbq(
            dataframe=df,
            destination_table=dataset_table,
            project_id=project_id,
            if_exists="append"
        )

        print(f"Successfully appended {len(df)} rows to BigQuery table: {dataset_table}")
        return True

    except Exception as e:
        print(f"Error loading data to BigQuery: {e}")
        return False


# Pipeline Execution
if __name__ == "__main__":
    input_file = os.path.join("data", "credit_risk_analytics.csv")
    output_file = os.path.join("data", "processed_loan_data.csv")

    GCP_PROJECT_ID = "credit-risk-analytics-504412"
    BIGQUERY_TABLE = "loan_portfolio.loan_clean"

    print("Starting Credit Risk ETL Pipeline...")
    
    raw_df = extract_data(input_file)
    if raw_df is not None:
        cleaned_df = transform_data(raw_df)
        if cleaned_df is not None:
            success = load_data(
                cleaned_df,
                output_file,
                GCP_PROJECT_ID,
                BIGQUERY_TABLE
            )
            
            if success:
                print("ETL Pipeline completed successfully!")