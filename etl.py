import os
import random
import pandas as pd
import pandas_gbq


# ============================================================
# 0. DATA SIMULATOR
# ============================================================

def simulate_daily_data(source_df, num_records=50):
    """
    Simulate incoming loan records using the existing
    cleaned + feature-engineered dataset.
    """

    # Select 50 random records
    df = source_df.sample(
        n=min(num_records, len(source_df)),
        random_state=random.randint(1, 10000)
    ).copy()

    # --------------------------------------------------------
    # Add small data quality issues for ETL testing
    # --------------------------------------------------------

    # Add missing employee titles
    if "emp_title" in df.columns and len(df) >= 3:
        df.loc[df.index[:3], "emp_title"] = None

    # Add extra spaces to employee titles
    if "emp_title" in df.columns and len(df) >= 6:
        df.loc[df.index[3:6], "emp_title"] = (
            "  "
            + df.loc[df.index[3:6], "emp_title"].astype(str)
            + "  "
        )

    # Add missing DTI values
    if "debt_to_income" in df.columns and len(df) >= 2:
        df.loc[df.index[:2], "debt_to_income"] = None

    # Add duplicate rows for testing
    duplicates = df.head(5).copy()

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )

    return df


# ============================================================
# 1. EXTRACT STEP
# ============================================================

def extract_data(file_path, use_simulation=True):
    """
    Extract data from the source CSV.
    """

    try:

        # Read source dataset
        source_df = pd.read_csv(file_path)

        print("Source dataset loaded successfully!")
        print(
            f"Source Rows: {source_df.shape[0]} | "
            f"Source Columns: {source_df.shape[1]}"
        )

        # Simulation mode
        if use_simulation:

            df = simulate_daily_data(
                source_df,
                num_records=50
            )

            print("\nSimulated incoming data created successfully!")
            print(
                f"Incoming Rows: {df.shape[0]} | "
                f"Incoming Columns: {df.shape[1]}"
            )

            return df

        # Real data mode
        else:

            print("\nReal data extracted successfully!")

            return source_df

    except Exception as e:

        print(f"Error loading data: {e}")

        return None


# ============================================================
# 2. TRANSFORM STEP
# ============================================================

def transform_data(df):
    """
    Clean and validate incoming loan data.
    """

    try:

        df_clean = df.copy()

        print("\nStarting data transformation...")

        # ----------------------------------------------------
        # Clean text columns
        # ----------------------------------------------------

        text_cols = df_clean.select_dtypes(
            include=["object"]
        ).columns

        for col in text_cols:

            df_clean[col] = (
                df_clean[col]
                .fillna("not_provided")
                .astype(str)
                .str.strip()
            )

        print("Text columns cleaned successfully!")


        # ----------------------------------------------------
        # Fill missing numeric values with 0
        # ----------------------------------------------------

        num_cols = df_clean.select_dtypes(
            include=["number"]
        ).columns

        for col in num_cols:

            df_clean[col] = df_clean[col].fillna(0)

        print("Missing numeric values handled successfully!")


        # ----------------------------------------------------
        # Remove duplicate rows
        # ----------------------------------------------------

        rows_before = len(df_clean)

        df_clean = df_clean.drop_duplicates()

        duplicates_removed = rows_before - len(df_clean)

        print(
            f"Duplicate records removed: "
            f"{duplicates_removed}"
        )


        # ----------------------------------------------------
        # Basic business validation
        # ----------------------------------------------------

        # Validate loan amount
        if "loan_amount" in df_clean.columns:

            before = len(df_clean)

            df_clean = df_clean[
                df_clean["loan_amount"] > 0
            ]

            print(
                f"Invalid loan amount records removed: "
                f"{before - len(df_clean)}"
            )


        # Validate annual income
        if "annual_income" in df_clean.columns:

            before = len(df_clean)

            df_clean = df_clean[
                df_clean["annual_income"] > 0
            ]

            print(
                f"Invalid annual income records removed: "
                f"{before - len(df_clean)}"
            )


        # Validate DTI
        if "debt_to_income" in df_clean.columns:

            before = len(df_clean)

            df_clean = df_clean[
                df_clean["debt_to_income"] >= 0
            ]

            print(
                f"Negative DTI records removed: "
                f"{before - len(df_clean)}"
            )


        print("\nData transformed successfully!")

        print(
            f"Final Rows: {df_clean.shape[0]} | "
            f"Final Columns: {df_clean.shape[1]}"
        )

        return df_clean

    except Exception as e:

        print(f"Error transforming data: {e}")

        return None


# ============================================================
# 3. LOAD STEP
# ============================================================

def load_data(
    df,
    output_path,
    project_id,
    dataset_table
):
    """
    Save processed data locally and append it to BigQuery.
    """

    try:

        # Save local CSV backup
        output_dir = os.path.dirname(output_path)

        if output_dir:
            os.makedirs(
                output_dir,
                exist_ok=True
            )

        df.to_csv(
            output_path,
            index=False
        )

        print("\nLocal backup CSV saved successfully!")
        print(f"Saved to: {output_path}")

        # Append data to BigQuery
        pandas_gbq.to_gbq(
            dataframe=df,
            destination_table=dataset_table,
            project_id=project_id,
            if_exists="append"
        )

        print("\nData appended successfully to BigQuery!")
        print(f"BigQuery Table: {dataset_table}")

        return True

    except Exception as e:

        print(f"Error loading data: {e}")

        return False


# ============================================================
# PIPELINE EXECUTION
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # FILE PATHS
    # --------------------------------------------------------

    input_file = (
        r"C:\Users\majji\Desktop"
        r"\Loan_Credit_Risk_Project"
        r"\data\credit_risk_analytics.csv"
    )

    output_file = (
        r"C:\Users\majji\Desktop"
        r"\Loan_Credit_Risk_Project"
        r"\data\processed_loan_data.csv"
    )


    # --------------------------------------------------------
    # BIGQUERY DETAILS
    # --------------------------------------------------------

    GCP_PROJECT_ID = "credit-risk-analytics-504412"

    BIGQUERY_TABLE = "loan_portfolio.loan_clean"


    print("=" * 50)
    print("STARTING LOAN CREDIT RISK ETL PIPELINE")
    print("=" * 50)


    # --------------------------------------------------------
    # EXTRACT + SIMULATE
    # --------------------------------------------------------

    raw_df = extract_data(
        file_path=input_file,
        use_simulation=True
    )


    # --------------------------------------------------------
    # TRANSFORM + LOAD
    # --------------------------------------------------------

    if raw_df is not None:

        cleaned_df = transform_data(raw_df)

        if cleaned_df is not None:

            load_success = load_data(
                df=cleaned_df,
                output_path=output_file,
                project_id=GCP_PROJECT_ID,
                dataset_table=BIGQUERY_TABLE
            )

            if load_success:
                print("\n" + "=" * 50)
                print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
                print("=" * 50)